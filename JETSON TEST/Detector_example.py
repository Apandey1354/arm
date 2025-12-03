import cv2
import numpy as np
import insightface
import os
from collections import deque
import time
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import json
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
from resemblyzer import VoiceEncoder, preprocess_wav
import threading
from sinch import SinchClient
import requests

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Try loading from root directory first, then backend directory
    if Path(".env").exists():
        load_dotenv(".env")
    elif Path("backend/.env").exists():
        load_dotenv("backend/.env")
    else:
        # Try both locations
        load_dotenv()
except ImportError:
    # dotenv not installed, will use os.getenv only
    pass


class FirebaseFaceDetector:
    def __init__(self, similarity_threshold=0.35, 
                 smoothing_frames=5, save_outputs=False, 
                 use_gpu=False, detection_size=320, frame_skip=1, 
                 process_resolution=480, voice_similarity_threshold=0.3,
                 enable_voice=True, voice_chunk_duration=1.0,
                 enable_sms=True, sinch_key_id=None, sinch_key_secret=None, 
                 sinch_project_id=None, sinch_from_number=None):
        """
        Face and voice detection system that loads embeddings from Firebase Firestore.
        
        Args:
            similarity_threshold: Minimum cosine similarity to consider a face match
            smoothing_frames: Number of frames to average similarity over
            save_outputs: Whether to save processed frames and embeddings
            use_gpu: Whether to use GPU for face detection
            detection_size: Size for face detection model
            frame_skip: Process every Nth frame (0 = all frames)
            process_resolution: Maximum resolution for processing
            voice_similarity_threshold: Minimum cosine similarity for voice match
            enable_voice: Whether to enable voice detection
            voice_chunk_duration: Duration in seconds for each voice detection chunk
        """
        self.similarity_threshold = similarity_threshold
        self.voice_similarity_threshold = voice_similarity_threshold
        self.smoothing_frames = smoothing_frames
        self.similarity_history = deque(maxlen=smoothing_frames)
        self.save_outputs = save_outputs
        self.frame_skip = frame_skip
        self.process_resolution = process_resolution
        self.detection_size = detection_size
        self.enable_voice = enable_voice
        self.voice_chunk_duration = voice_chunk_duration
        
        # Initialize InsightFace
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if use_gpu else ['CPUExecutionProvider']
        self.app = insightface.app.FaceAnalysis(name='buffalo_l', providers=providers)
        self.app.prepare(ctx_id=-1 if use_gpu else 0, det_size=(detection_size, detection_size))
        
        # Initialize Voice Encoder
        if self.enable_voice:
            print("🎤 Initializing voice encoder...")
            self.voice_encoder = VoiceEncoder()
            print("✅ Voice encoder initialized")
            self.sample_rate = 16000
            self.listening = False
            self.voice_thread = None
            self.current_voice_matches = []  # Changed to list to support multiple speakers
            self.voice_similarity_history = deque(maxlen=5)
            self.voice_match_history = {}  # Track matches over time: {name: {'similarity': float, 'count': int, 'last_seen': time, 'first_detected': time}}
            self.active_speakers = {}  # Track currently active speakers: {name: {'similarity': float, 'last_update': time}}
            self.speaker_timeout = 2.0  # Remove speaker after 2 seconds of no detection (faster for crowded places)
        
        # Setup output directories if needed
        if self.save_outputs:
            self.output_dir = Path("saved_processing")
            self.output_dir.mkdir(exist_ok=True)
            self.embeddings_dir = self.output_dir / "embeddings"
            self.embeddings_dir.mkdir(exist_ok=True)
            self.frames_dir = self.output_dir / "processed_frames"
            self.frames_dir.mkdir(exist_ok=True)
        
        # Initialize Firebase
        self.db = self.initialize_firebase()
        
        # Download and load embeddings from Firebase (only once at startup)
        print("\n" + "="*60)
        print("📥 DOWNLOADING EMBEDDINGS FROM FIREBASE...")
        print("="*60)
        self.reference_embeddings, self.reference_names, self.reference_info, \
        self.voice_embeddings, self.voice_names, self.voice_info = self.download_embeddings_from_firebase()
        self.reference_embeddings_array = np.array(self.reference_embeddings) if len(self.reference_embeddings) > 0 else None
        self.voice_embeddings_array = np.array(self.voice_embeddings) if len(self.voice_embeddings) > 0 else None
        
        print(f"✅ Loaded {len(self.reference_embeddings)} face embeddings into memory")
        if self.enable_voice:
            print(f"✅ Loaded {len(self.voice_embeddings)} voice embeddings into memory")
        print("✅ All matching will now use local embeddings (no Firebase queries during detection)")
        print("="*60 + "\n")
        
        self.frame_counter = 0
        self.fps_history = deque(maxlen=30)
        self.last_time = time.time()
        
        # Cache for smoother rendering
        self.last_faces_data = []  # Store last detected faces data
        self.frame_cache = None  # Cache last processed frame
        self.last_detection_time = 0
        
        # Tracking for continuous detection and image saving
        self.detection_timers = {}  # Track when each person was first detected: {name: first_detection_time}
        self.saved_persons = set()  # Track which persons have already been saved
        self.save_duration = 10.0  # Save after 10 seconds of continuous detection
        self.storage_dir = Path("detected_persons")
        self.storage_dir.mkdir(exist_ok=True)
        print(f"📁 Images will be saved to: {self.storage_dir.absolute()}")
        
        # SMS Configuration
        self.enable_sms = enable_sms
        self.sms_cooldown = 3600.0  # Don't send SMS for same person more than once per hour (3600 seconds)
        self.sms_sent_times = {}  # Track when SMS was last sent for each person: {person_key: last_sms_time}
        
        # Initialize Sinch Client if SMS is enabled
        if self.enable_sms:
            # Try to read from sinch_config.txt file if it exists
            sinch_config_file = Path("sinch_config.txt")
            if sinch_config_file.exists() and not (sinch_key_id or sinch_key_secret or sinch_project_id):
                try:
                    with open(sinch_config_file, 'r') as f:
                        lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith('#')]
                        if len(lines) >= 3:
                            sinch_key_id = sinch_key_id or lines[0] if not sinch_key_id else sinch_key_id
                            sinch_key_secret = sinch_key_secret or lines[1] if len(lines) > 1 and not sinch_key_secret else sinch_key_secret
                            sinch_project_id = sinch_project_id or lines[2] if len(lines) > 2 and not sinch_project_id else sinch_project_id
                            sinch_from_number = sinch_from_number or lines[3] if len(lines) > 3 and not sinch_from_number else sinch_from_number
                            print("✅ Loaded Sinch credentials from sinch_config.txt")
                except Exception as e:
                    print(f"⚠️  Could not read sinch_config.txt: {e}")
            
            # Load from parameters, then .env file, then environment variables
            self.sinch_key_id = sinch_key_id or os.getenv("SINCH_KEY_ID") or os.getenv("sinch_key_id")
            self.sinch_key_secret = sinch_key_secret or os.getenv("SINCH_KEY_SECRET") or os.getenv("sinch_key_secret")
            self.sinch_project_id = sinch_project_id or os.getenv("SINCH_PROJECT_ID") or os.getenv("sinch_project_id")
            self.sinch_from_number = sinch_from_number or os.getenv("SINCH_FROM_NUMBER") or os.getenv("sinch_from_number")
            
            # Debug: Show what was loaded (without exposing secrets)
            if self.enable_sms:
                print(f"🔍 Checking Sinch credentials...")
                print(f"   Key ID: {'✅ Found' if self.sinch_key_id else '❌ Missing'}")
                print(f"   Key Secret: {'✅ Found' if self.sinch_key_secret else '❌ Missing'}")
                print(f"   Project ID: {'✅ Found' if self.sinch_project_id else '❌ Missing'}")
                print(f"   From Number: {'✅ Found' if self.sinch_from_number else '⚠️  Optional'}")
            
            if self.sinch_key_id and self.sinch_key_secret and self.sinch_project_id:
                try:
                    self.sinch_client = SinchClient(
                        key_id=self.sinch_key_id,
                        key_secret=self.sinch_key_secret,
                        project_id=self.sinch_project_id
                    )
                    print("✅ Sinch SMS client initialized")
                    if self.sinch_from_number:
                        print(f"   From number: {self.sinch_from_number}")
                    else:
                        print("   ⚠️  SINCH_FROM_NUMBER not set - SMS may fail")
                except Exception as e:
                    print(f"❌ Error initializing Sinch client: {e}")
                    self.enable_sms = False
            else:
                missing = []
                if not self.sinch_key_id:
                    missing.append("SINCH_KEY_ID")
                if not self.sinch_key_secret:
                    missing.append("SINCH_KEY_SECRET")
                if not self.sinch_project_id:
                    missing.append("SINCH_PROJECT_ID")
                print(f"⚠️  Sinch credentials not found. Missing: {', '.join(missing)}")
                print("   Options:")
                print("   1. Create sinch_config.txt with 4 lines: key_id, key_secret, project_id, from_number")
                print("   2. Set environment variables: SINCH_KEY_ID, SINCH_KEY_SECRET, SINCH_PROJECT_ID, SINCH_FROM_NUMBER")
                print("   3. Pass credentials directly as parameters to FirebaseFaceDetector()")
                self.enable_sms = False
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK."""
        # Check if already initialized
        if not firebase_admin._apps:
            cred = None
            
            # Check if using service account key file
            if os.path.exists("backend/serviceAccountKey.json"):
                try:
                    cred = credentials.Certificate("backend/serviceAccountKey.json")
                    print("✅ Firebase credentials loaded from serviceAccountKey.json")
                except Exception as e:
                    print(f"❌ Error loading serviceAccountKey.json: {e}")
            
            # Check if using environment variable
            elif os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"):
                try:
                    service_account_info = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"))
                    cred = credentials.Certificate(service_account_info)
                    print("✅ Firebase credentials loaded from environment variable")
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing FIREBASE_SERVICE_ACCOUNT_KEY: Invalid JSON - {e}")
                except Exception as e:
                    print(f"❌ Error loading credentials from environment variable: {e}")
            
            # If no credentials found, show error
            if cred is None:
                raise Exception(
                    "Firebase credentials not found. "
                    "Please set up serviceAccountKey.json in backend/ directory or "
                    "FIREBASE_SERVICE_ACCOUNT_KEY environment variable."
                )
            
            try:
                firebase_admin.initialize_app(cred)
                print("✅ Firebase Admin SDK initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing Firebase: {e}")
                raise
        
        try:
            db = firestore.client()
            print("✅ Firestore client connected")
            return db
        except Exception as e:
            print(f"❌ Error connecting to Firestore: {e}")
            raise
    
    def download_embeddings_from_firebase(self):
        """
        Download all face and voice embeddings from Firebase Firestore 'upload' collection.
        This is done ONCE at startup - all subsequent matching uses local data.
        
        Returns:
            face_embeddings: List of face embedding arrays
            face_names: List of person names for faces
            face_info: List of additional info for faces
            voice_embeddings: List of voice embedding arrays
            voice_names: List of person names for voices
            voice_info: List of additional info for voices
        """
        face_embeddings = []
        face_names = []
        face_info = []
        voice_embeddings = []
        voice_names = []
        voice_info = []
        
        try:
            print("📡 Connecting to Firebase Firestore...")
            # Get all documents from 'upload' collection
            uploads_ref = self.db.collection("upload")
            docs = uploads_ref.stream()
            
            total_docs = 0
            total_face_embeddings = 0
            total_voice_embeddings = 0
            
            print("📥 Downloading documents...")
            for doc in docs:
                total_docs += 1
                doc_data = doc.to_dict()
                
                # Get person information
                full_name = doc_data.get("fullName", "Unknown")
                age = doc_data.get("age", "N/A")
                city = doc_data.get("cityLastSeen", "N/A")
                date_seen = doc_data.get("dateLastSeen", "N/A")
                contact = doc_data.get("contactPhone", "N/A")
                
                # Extract face embeddings from imageMetadata
                image_metadata = doc_data.get("imageMetadata", [])
                
                for img_meta in image_metadata:
                    if img_meta.get("has_face", False) and img_meta.get("embedding") is not None:
                        embedding = np.array(img_meta.get("embedding"))
                        face_embeddings.append(embedding)
                        face_names.append(full_name)
                        face_info.append({
                            "name": full_name,
                            "age": age,
                            "city": city,
                            "dateSeen": date_seen,
                            "contact": contact,
                            "docId": doc.id,
                            "imageIndex": img_meta.get("index", 0),
                            "type": "face"
                        })
                        total_face_embeddings += 1
                        print(f"  ✓ Downloaded face embedding for: {full_name} (Doc #{total_docs}, Face #{total_face_embeddings})")
                
                # Extract voice embeddings from audioMetadata
                audio_metadata = doc_data.get("audioMetadata")
                if audio_metadata and audio_metadata.get("has_voice", False) and audio_metadata.get("embedding") is not None:
                    voice_embedding = np.array(audio_metadata.get("embedding"))
                    voice_embeddings.append(voice_embedding)
                    voice_names.append(full_name)
                    voice_info.append({
                        "name": full_name,
                        "age": age,
                        "city": city,
                        "dateSeen": date_seen,
                        "contact": contact,
                        "docId": doc.id,
                        "type": "voice"
                    })
                    total_voice_embeddings += 1
                    print(f"  ✓ Downloaded voice embedding for: {full_name} (Doc #{total_docs}, Voice #{total_voice_embeddings})")
            
            print(f"\n✅ Download complete:")
            print(f"   - {total_face_embeddings} face embeddings from {total_docs} documents")
            if self.enable_voice:
                print(f"   - {total_voice_embeddings} voice embeddings from {total_docs} documents")
            
            if len(face_embeddings) == 0 and len(voice_embeddings) == 0:
                print("⚠️  No embeddings found in Firebase. Make sure you have uploaded missing person data.")
            
            return face_embeddings, face_names, face_info, voice_embeddings, voice_names, voice_info
            
        except Exception as e:
            print(f"❌ Error downloading embeddings from Firebase: {e}")
            return [], [], [], [], [], []
    
    def reload_embeddings_from_firebase(self):
        """
        Reload embeddings from Firebase (useful when new data is added).
        This replaces the local embeddings with fresh data from Firebase.
        """
        print("\n" + "="*60)
        print("🔄 RELOADING EMBEDDINGS FROM FIREBASE...")
        print("="*60)
        self.reference_embeddings, self.reference_names, self.reference_info, \
        self.voice_embeddings, self.voice_names, self.voice_info = self.download_embeddings_from_firebase()
        self.reference_embeddings_array = np.array(self.reference_embeddings) if len(self.reference_embeddings) > 0 else None
        self.voice_embeddings_array = np.array(self.voice_embeddings) if len(self.voice_embeddings) > 0 else None
        print(f"✅ Reloaded {len(self.reference_embeddings)} face embeddings into memory")
        if self.enable_voice:
            print(f"✅ Reloaded {len(self.voice_embeddings)} voice embeddings into memory")
        print("="*60 + "\n")
    
    def compute_max_similarity_vectorized(self, embedding):
        """
        Compute cosine similarity between input embedding and all LOCAL reference embeddings.
        This uses ONLY the downloaded embeddings (no Firebase queries).
        
        Returns:
            similarity: Best match similarity score
            best_match_idx: Index of best match
        """
        if self.reference_embeddings_array is None or len(self.reference_embeddings_array) == 0:
            return 0.0, None
        
        embedding_norm = np.linalg.norm(embedding)
        if embedding_norm == 0:
            return 0.0, None
        
        # Compute cosine similarity using LOCAL embeddings only
        similarities = np.dot(self.reference_embeddings_array, embedding) / (
            np.linalg.norm(self.reference_embeddings_array, axis=1) * embedding_norm
        )
        
        best_match_idx = int(np.argmax(similarities))
        return float(similarities[best_match_idx]), best_match_idx
    
    def compute_voice_similarity(self, voice_embedding):
        """
        Compute cosine similarity between input voice embedding and all LOCAL voice embeddings.
        
        Returns:
            similarity: Best match similarity score
            best_match_idx: Index of best match
        """
        if not self.enable_voice or self.voice_embeddings_array is None or len(self.voice_embeddings_array) == 0:
            return 0.0, None
        
        embedding_norm = np.linalg.norm(voice_embedding)
        if embedding_norm == 0:
            return 0.0, None
        
        # Compute cosine similarity using LOCAL voice embeddings only
        similarities = np.dot(self.voice_embeddings_array, voice_embedding) / (
            np.linalg.norm(self.voice_embeddings_array, axis=1) * embedding_norm
        )
        
        best_match_idx = int(np.argmax(similarities))
        return float(similarities[best_match_idx]), best_match_idx
    
    def compute_all_voice_matches(self, voice_embedding, threshold=None):
        """
        Compute cosine similarity for ALL voice embeddings and return all matches above threshold.
        This allows detecting multiple speakers.
        
        Returns:
            matches: List of tuples (similarity, index, name, info) for all matches above threshold
        """
        if not self.enable_voice or self.voice_embeddings_array is None or len(self.voice_embeddings_array) == 0:
            return []
        
        if threshold is None:
            threshold = self.voice_similarity_threshold
        
        embedding_norm = np.linalg.norm(voice_embedding)
        if embedding_norm == 0:
            return []
        
        # Compute cosine similarity for ALL embeddings
        similarities = np.dot(self.voice_embeddings_array, voice_embedding) / (
            np.linalg.norm(self.voice_embeddings_array, axis=1) * embedding_norm
        )
        
        # Find all matches above threshold
        matches = []
        for idx, similarity in enumerate(similarities):
            if similarity > threshold:
                matches.append({
                    'similarity': float(similarity),
                    'index': idx,
                    'name': self.voice_names[idx],
                    'info': self.voice_info[idx]
                })
        
        # Sort by similarity (highest first)
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        
        return matches
    
    def voice_listen_loop(self):
        """
        Real-time voice detection loop running in a separate thread.
        """
        while self.listening:
            try:
                # Record audio chunk
                audio = sd.rec(int(self.sample_rate * self.voice_chunk_duration),
                              samplerate=self.sample_rate, channels=1, dtype='float32')
                sd.wait()
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                    temp_path = temp_file.name
                    try:
                        # Convert to int16 for WAV format
                        audio_int16 = (audio * 32767).astype(np.int16)
                        write(temp_path, self.sample_rate, audio_int16)
                        
                        # Preprocess and extract embedding
                        wav = preprocess_wav(temp_path)
                        live_embedding = self.voice_encoder.embed_utterance(wav)
                        
                        # Find ALL matches above threshold (not just the best one)
                        all_matches = self.compute_all_voice_matches(live_embedding)
                        
                        # Update voice match history and active speakers
                        current_time = time.time()
                        detected_names = set()
                        
                        # Process all matches found in this chunk
                        for match in all_matches:
                            name = match['name']
                            similarity = match['similarity']
                            detected_names.add(name)
                            
                            # Update active speakers (for real-time display)
                            self.active_speakers[name] = {
                                'similarity': similarity,
                                'last_update': current_time,
                                'info': match['info']
                            }
                            
                            # Update or create history entry
                            if name not in self.voice_match_history:
                                self.voice_match_history[name] = {
                                    'similarity': similarity,
                                    'count': 1,
                                    'last_seen': current_time,
                                    'first_detected': current_time,
                                    'info': match['info']
                                }
                            else:
                                # Update with exponential moving average
                                old_sim = self.voice_match_history[name]['similarity']
                                new_sim = 0.7 * old_sim + 0.3 * similarity  # Smoothing
                                self.voice_match_history[name]['similarity'] = new_sim
                                self.voice_match_history[name]['count'] += 1
                                self.voice_match_history[name]['last_seen'] = current_time
                        
                        # Remove active speakers that haven't been detected recently (faster timeout for crowded places)
                        active_speakers_to_remove = [
                            name for name, data in self.active_speakers.items()
                            if (current_time - data['last_update']) > self.speaker_timeout
                        ]
                        for name in active_speakers_to_remove:
                            del self.active_speakers[name]
                        
                        # Remove matches from history that haven't been seen recently
                        history_timeout = 5.0  # Keep in history longer for context
                        names_to_remove = [
                            name for name, data in self.voice_match_history.items()
                            if (current_time - data['last_seen']) > history_timeout and name not in detected_names
                        ]
                        for name in names_to_remove:
                            del self.voice_match_history[name]
                        
                        # Update current voice matches list - prioritize active speakers
                        # First, add active speakers (currently speaking)
                        active_matches = [
                            {
                                'name': name,
                                'similarity': data['similarity'],
                                'info': data['info'],
                                'is_active': True,
                                'last_update': data['last_update']
                            }
                            for name, data in self.active_speakers.items()
                            if data['similarity'] > self.voice_similarity_threshold
                        ]
                        
                        # Then add recent matches from history (recently detected)
                        recent_matches = [
                            {
                                'name': name,
                                'similarity': data['similarity'],
                                'info': data['info'],
                                'is_active': False,
                                'last_seen': data['last_seen']
                            }
                            for name, data in self.voice_match_history.items()
                            if name not in self.active_speakers and 
                               data['similarity'] > self.voice_similarity_threshold and
                               (current_time - data['last_seen']) < 3.0  # Show recent matches within 3 seconds
                        ]
                        
                        # Combine and sort: active speakers first, then by similarity
                        self.current_voice_matches = active_matches + recent_matches
                        self.current_voice_matches.sort(key=lambda x: (not x.get('is_active', False), -x['similarity']))
                            
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_path):
                            try:
                                os.unlink(temp_path)
                            except:
                                pass
                
                # No sleep - process continuously for real-time detection in crowded places
                # The audio recording itself provides natural pacing
                
            except Exception as e:
                print(f"Error in voice detection: {e}")
                time.sleep(1)
    
    def start_voice_detection(self):
        """Start voice detection in a separate thread."""
        if not self.enable_voice:
            return
        
        if self.voice_embeddings_array is None or len(self.voice_embeddings_array) == 0:
            print("⚠️  No voice embeddings loaded. Voice detection disabled.")
            return
        
        if not self.listening:
            self.listening = True
            self.voice_thread = threading.Thread(target=self.voice_listen_loop, daemon=True)
            self.voice_thread.start()
            print("🎤 Voice detection started")
    
    def stop_voice_detection(self):
        """Stop voice detection."""
        if self.listening:
            self.listening = False
            if self.voice_thread:
                self.voice_thread.join(timeout=2)
            print("🎤 Voice detection stopped")
    
    def save_detected_person_image(self, frame, person_key, name, match_info, x1, y1, x2, y2):
        """
        Save image of detected person after 10 seconds of continuous detection.
        
        Args:
            frame: Full frame from camera
            person_key: Unique key for the person
            name: Person's name
            match_info: Additional information about the person
            x1, y1, x2, y2: Bounding box coordinates
        """
        try:
            # Extract person region with some padding
            padding = 20
            h, w = frame.shape[:2]
            crop_x1 = max(0, x1 - padding)
            crop_y1 = max(0, y1 - padding)
            crop_x2 = min(w, x2 + padding)
            crop_y2 = min(h, y2 + padding)
            
            # Crop the person from the frame
            person_crop = frame[crop_y1:crop_y2, crop_x1:crop_x2]
            
            # Create filename with timestamp and person name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            filename = f"{safe_name}_{timestamp}_{person_key[:8]}.jpg"
            filepath = self.storage_dir / filename
            
            # Save the image
            cv2.imwrite(str(filepath), person_crop)
            
            # Also save full frame with annotation
            full_frame_filename = f"{safe_name}_{timestamp}_FULL.jpg"
            full_frame_path = self.storage_dir / full_frame_filename
            
            # Draw annotation on full frame
            annotated_frame = frame.copy()
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.putText(annotated_frame, f"{name} - SAVED", (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imwrite(str(full_frame_path), annotated_frame)
            
            print(f"💾 SAVED: {name} - {filepath.name}")
            print(f"💾 SAVED (Full Frame): {full_frame_filename}")
            
            # Create info file with person details
            info_filename = f"{safe_name}_{timestamp}_INFO.txt"
            info_path = self.storage_dir / info_filename
            with open(info_path, 'w') as f:
                f.write(f"Detected Person Information\n")
                f.write(f"{'='*50}\n\n")
                f.write(f"Name: {name}\n")
                f.write(f"Age: {match_info.get('age', 'N/A')}\n")
                f.write(f"City: {match_info.get('city', 'N/A')}\n")
                f.write(f"Date Last Seen: {match_info.get('dateSeen', 'N/A')}\n")
                f.write(f"Contact: {match_info.get('contact', 'N/A')}\n")
                f.write(f"Document ID: {match_info.get('docId', 'N/A')}\n")
                f.write(f"Detection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Cropped Image: {filename}\n")
                f.write(f"Full Frame: {full_frame_filename}\n")
            
            print(f"📄 Info saved: {info_filename}")
            
        except Exception as e:
            print(f"❌ Error saving image for {name}: {e}")
    
    def get_smoothed_similarity(self, current_similarity):
        """Apply temporal smoothing to similarity scores."""
        self.similarity_history.append(current_similarity)
        return np.mean(self.similarity_history)
    
    def get_location_info(self):
        """
        Get current location coordinates and address information.
        Uses IP-based geolocation as fallback if GPS is not available.
        
        Returns:
            dict: {'latitude': float, 'longitude': float, 'address': str, 'city': str, 'country': str}
        """
        try:
            # Try to get location from IP-based geolocation service
            response = requests.get('http://ip-api.com/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'latitude': data.get('lat', 0.0),
                    'longitude': data.get('lon', 0.0),
                    'address': f"{data.get('city', 'Unknown')}, {data.get('regionName', 'Unknown')}",
                    'city': data.get('city', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'zip': data.get('zip', 'Unknown')
                }
        except Exception as e:
            print(f"⚠️  Could not get location from IP geolocation: {e}")
        
        # Fallback to default/unknown location
        return {
            'latitude': 0.0,
            'longitude': 0.0,
            'address': 'Location unavailable',
            'city': 'Unknown',
            'country': 'Unknown',
            'zip': 'Unknown'
        }
    
    def send_sms_notification(self, person_name, match_info, location_info):
        """
        Send SMS notification with person detection and location information.
        
        Args:
            person_name: Name of the detected person
            match_info: Additional information about the person
            location_info: Location information dictionary
        """
        if not self.enable_sms:
            print(f"⚠️  SMS is disabled. Cannot send SMS for {person_name}.")
            return False
        
        if not hasattr(self, 'sinch_client') or self.sinch_client is None:
            print(f"❌ Sinch client not initialized. Cannot send SMS for {person_name}.")
            return False
        
        # Get contact number from match_info
        contact_number = match_info.get('contact', '').strip()
        if not contact_number:
            print(f"⚠️  No contact number found for {person_name}. Cannot send SMS.")
            return False
        
        # Format phone number (ensure it starts with +)
        if not contact_number.startswith('+'):
            # Assume it's a US number if no country code
            if contact_number.startswith('1'):
                contact_number = '+' + contact_number
            else:
                contact_number = '+1' + contact_number.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        # Create SMS message with only name, age, and coordinates
        message = f"{person_name}\n{match_info.get('age', 'N/A')}\n{location_info['latitude']:.6f},{location_info['longitude']:.6f}"

        try:
            send_batch_response = self.sinch_client.sms.batches.send(
                body=message,
                to=[contact_number],
                from_=self.sinch_from_number,
                delivery_report="none"
            )
            print(f"✅ SMS sent to {contact_number} for {person_name}")
            print(f"   Response: {send_batch_response}")
            return True
        except Exception as e:
            print(f"❌ Error sending SMS to {contact_number} for {person_name}: {e}")
            return False
    
    def resize_for_processing(self, frame):
        """Resize frame for processing while maintaining aspect ratio."""
        h, w = frame.shape[:2]
        if max(h, w) > self.process_resolution:
            scale = self.process_resolution / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        return frame
    
    def process_frame(self, frame, frame_count=0):
        """
        Process a single frame for face detection and recognition.
        Handles MULTIPLE faces in the frame with optimized performance.
        
        Returns:
            frame: Processed frame with bounding boxes and labels for all faces
        """
        self.frame_counter += 1
        current_time = time.time()
        
        # Always update FPS for smooth display
        fps = 1.0 / (current_time - self.last_time) if self.last_time > 0 else 0
        self.fps_history.append(fps)
        self.last_time = current_time
        avg_fps = np.mean(self.fps_history) if len(self.fps_history) > 0 else 0
        
        # Create a copy of frame for drawing (prevents flickering)
        display_frame = frame.copy()
        
        # Decide whether to run detection or use cached results
        should_detect = (self.frame_counter % (self.frame_skip + 1) == 0) or \
                        (current_time - self.last_detection_time > 0.1)  # Force detection every 100ms
        
        if should_detect:
            # Resize for processing (smaller = faster)
            processed_frame = self.resize_for_processing(frame)
            faces = self.app.get(processed_frame)
            
            # Calculate scale factors for bounding box
            scale_x = frame.shape[1] / processed_frame.shape[1]
            scale_y = frame.shape[0] / processed_frame.shape[0]
            
            # Store faces data for caching
            self.last_faces_data = []
            
            if len(faces) > 0:
                # Process ALL detected faces
                for face_idx, face in enumerate(faces):
                    embedding = face.embedding
                    
                    # Find best match for this face
                    similarity, best_match_idx = self.compute_max_similarity_vectorized(embedding)
                    smoothed_similarity = self.get_smoothed_similarity(similarity)
                    
                    # Determine name and match status
                    name = "Unknown"
                    match_info = None
                    
                    if best_match_idx is not None and smoothed_similarity > self.similarity_threshold:
                        name = self.reference_names[best_match_idx]
                        match_info = self.reference_info[best_match_idx]
                    
                    # Scale bounding box back to original frame size
                    bbox = (face.bbox * np.array([scale_x, scale_y, scale_x, scale_y])).astype(int)
                    x1, y1, x2, y2 = bbox
                    
                    # Store face data for caching
                    self.last_faces_data.append({
                        'bbox': (x1, y1, x2, y2),
                        'name': name,
                        'similarity': smoothed_similarity,
                        'match_info': match_info,
                        'is_match': name != "Unknown"
                    })
            
            self.last_detection_time = current_time
        
        # Track currently detected persons
        current_detected_names = set()
        
        # Draw cached or current faces data
        for face_data in self.last_faces_data:
            x1, y1, x2, y2 = face_data['bbox']
            name = face_data['name']
            similarity = face_data['similarity']
            match_info = face_data['match_info']
            is_match = face_data['is_match']
            
            # Track detected persons for continuous detection
            if is_match and name != "Unknown":
                person_key = f"{name}_{match_info.get('docId', 'unknown')}"
                current_detected_names.add(person_key)
                
                # Start or continue tracking detection time
                is_new_detection = person_key not in self.detection_timers
                if is_new_detection:
                    self.detection_timers[person_key] = {
                        'first_detection': current_time,
                        'name': name,
                        'info': match_info
                    }
                    print(f"⏱️  Started tracking: {name}")
                    
                    # Send SMS immediately when person is first detected (if cooldown allows)
                    if self.enable_sms:
                        last_sms_time = self.sms_sent_times.get(person_key, 0)
                        time_since_last_sms = current_time - last_sms_time
                        
                        print(f"🔍 SMS check for {name}: last_sms_time={last_sms_time}, time_since={time_since_last_sms:.1f}s, cooldown={self.sms_cooldown}s")
                        
                        # Check if we can send SMS (either never sent, or cooldown expired)
                        if time_since_last_sms >= self.sms_cooldown or last_sms_time == 0:
                            print(f"✅ SMS cooldown passed or never sent. Getting location and sending SMS for {name}...")
                            # Get current location
                            location_info = self.get_location_info()
                            
                            # Send SMS notification
                            if self.send_sms_notification(name, match_info, location_info):
                                # Update last SMS time
                                self.sms_sent_times[person_key] = current_time
                                print(f"📱 SMS sent successfully for {name} at {location_info['address']}")
                            else:
                                print(f"❌ Failed to send SMS for {name}")
                        else:
                            remaining_cooldown = (self.sms_cooldown - time_since_last_sms) / 60
                            print(f"⏳ SMS cooldown active for {name}. Next SMS available in {remaining_cooldown:.1f} minutes")
                    else:
                        print(f"⚠️  SMS is disabled. Enable SMS to send notifications for {name}")
                
                # Check if 10 seconds have passed (for image saving)
                detection_duration = current_time - self.detection_timers[person_key]['first_detection']
                
                if detection_duration >= self.save_duration and person_key not in self.saved_persons:
                    # Save the image
                    self.save_detected_person_image(display_frame, person_key, name, match_info, x1, y1, x2, y2)
                    self.saved_persons.add(person_key)
            
            # Determine color and label
            color = (0, 255, 0) if is_match else (0, 0, 255)
            label = f"{name}" if is_match else "Unknown"
            
            # Draw bounding box with slight transparency effect (thicker for visibility)
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 3)
            
            # Draw label with similarity score (with background for readability)
            label_text = f"{label} ({similarity:.2f})"
            (text_width, text_height), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            cv2.rectangle(display_frame, (x1, y1 - text_height - 15), 
                         (x1 + text_width, y1), color, -1)
            cv2.putText(display_frame, label_text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Draw detection timer if person is being tracked
            if is_match and name != "Unknown":
                person_key = f"{name}_{match_info.get('docId', 'unknown')}"
                if person_key in self.detection_timers:
                    detection_duration = current_time - self.detection_timers[person_key]['first_detection']
                    timer_text = f"Detected: {detection_duration:.1f}s"
                    if person_key in self.saved_persons:
                        timer_text = "✓ SAVED"
                    (timer_width, timer_height), _ = cv2.getTextSize(timer_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(display_frame, (x1, y2 + 5), 
                                 (x1 + timer_width + 10, y2 + timer_height + 10), (0, 255, 255), -1)
                    cv2.putText(display_frame, timer_text, (x1 + 5, y2 + timer_height + 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
            # Draw additional info if match found
            if is_match and match_info:
                info_text = f"Age: {match_info['age']} | City: {match_info['city']}"
                (info_width, info_height), _ = cv2.getTextSize(info_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(display_frame, (x1, y2 + 15), 
                             (x1 + info_width, y2 + 35), color, -1)
                cv2.putText(display_frame, info_text, (x1, y2 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                contact_text = f"Contact: {match_info['contact']}"
                (contact_width, contact_height), _ = cv2.getTextSize(contact_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(display_frame, (x1, y2 + 40), 
                             (x1 + contact_width, y2 + 60), color, -1)
                cv2.putText(display_frame, contact_text, (x1, y2 + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Remove timers for persons no longer detected
        persons_to_remove = [key for key in self.detection_timers.keys() if key not in current_detected_names]
        for key in persons_to_remove:
            del self.detection_timers[key]
            # Don't remove from saved_persons to prevent re-saving
            # Don't remove from sms_sent_times to maintain cooldown tracking
        
        # Display FPS and face count with background for readability
        fps_text = f"FPS: {avg_fps:.1f}"
        faces_text = f"Faces: {len(self.last_faces_data)}"
        
        # Calculate dynamic info height based on number of voices
        info_height = 80
        if self.enable_voice:
            if len(self.current_voice_matches) > 0:
                max_voices_to_show = min(5, len(self.current_voice_matches))
                info_height = 80 + (max_voices_to_show * 25) + 10  # Extra space for "more" indicator
                if info_height > 220:
                    info_height = 220  # Max height
            else:
                info_height = 110
        
        # Draw background rectangles for text
        cv2.rectangle(display_frame, (5, 5), (350, info_height), (0, 0, 0), -1)
        cv2.putText(display_frame, fps_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, faces_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display voice matches (can be multiple speakers) - optimized for crowded places
        if self.enable_voice:
            if len(self.current_voice_matches) > 0:
                # Display all detected voices
                y_offset = 90
                max_voices_to_show = min(5, len(self.current_voice_matches))  # Show up to 5 speakers in crowded places
                
                for i, match in enumerate(self.current_voice_matches[:max_voices_to_show]):
                    is_active = match.get('is_active', False)
                    
                    # Different colors for active vs recent speakers
                    if is_active:
                        # Active speaker (currently speaking) - brighter yellow
                        color = (0, 255, 255)  # Cyan for active
                        voice_text = f"🔊 {match['name']} ({match['similarity']:.2f})"
                    else:
                        # Recent speaker (recently detected) - yellow
                        color = (255, 255, 0)  # Yellow for recent
                        voice_text = f"   {match['name']} ({match['similarity']:.2f})"
                    
                    cv2.putText(display_frame, voice_text, (10, y_offset),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    y_offset += 25
                
                # Show count if more speakers detected
                if len(self.current_voice_matches) > max_voices_to_show:
                    more_text = f"... +{len(self.current_voice_matches) - max_voices_to_show} more"
                    cv2.putText(display_frame, more_text, (10, y_offset),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (128, 128, 128), 1)
            else:
                cv2.putText(display_frame, "Voice: Listening...", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 128, 128), 2)
        
        return display_frame
    
    def run(self, video_source=0):
        """
        Run face detection on video source.
        
        Args:
            video_source: Video source (0 for webcam, or path to video file)
        """
        if len(self.reference_embeddings) == 0:
            print("❌ No embeddings loaded from Firebase. Cannot run detection.")
            return
        
        try:
            cv2.namedWindow('Firebase Face & Voice Detection', cv2.WINDOW_NORMAL)
        except cv2.error:
            print("GUI Error. Fix by reinstalling OpenCV.")
            return
        
        cap = cv2.VideoCapture(video_source)
        if not cap.isOpened():
            print(f"Could not open video source: {video_source}")
            return
        
        print("\n" + "="*60)
        print("🎥 STARTING FACE & VOICE DETECTION")
        print("="*60)
        print(f"📊 Using {len(self.reference_embeddings)} face embeddings (downloaded from Firebase)")
        if self.enable_voice:
            print(f"🎤 Using {len(self.voice_embeddings)} voice embeddings (downloaded from Firebase)")
        print(f"🎯 Face similarity threshold: {self.similarity_threshold}")
        if self.enable_voice:
            print(f"🎯 Voice similarity threshold: {self.voice_similarity_threshold}")
        print(f"⏱️  Voice chunk duration: {self.voice_chunk_duration}s (optimized for crowded places)")
        print(f"⚡ All matching is done locally (no Firebase queries during detection)")
        print(f"⚡ Optimized for real-time detection in crowded environments")
        print(f"👥 Detects ALL speakers from database simultaneously")
        print("\nControls:")
        print("  'q' - Quit")
        print("  'r' - Reload embeddings from Firebase")
        print("  'v' - Toggle voice detection")
        print("="*60 + "\n")
        
        # Start voice detection if enabled
        if self.enable_voice:
            self.start_voice_detection()
        
        # Set camera properties for smoother video
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for lower latency
        
        frame_count = 0
        target_fps = 30
        frame_time = 1.0 / target_fps
        
        while True:
            loop_start = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            frame = self.process_frame(frame, frame_count)
            
            # Display frame
            cv2.imshow('Firebase Face & Voice Detection', frame)
            
            frame_count += 1
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                # Reload embeddings from Firebase
                self.reload_embeddings_from_firebase()
                # Restart voice detection if it was running
                if self.enable_voice and not self.listening:
                    self.start_voice_detection()
            elif key == ord('v'):
                # Toggle voice detection
                if self.enable_voice:
                    if self.listening:
                        self.stop_voice_detection()
                    else:
                        self.start_voice_detection()
                # Restart voice detection if it was running
                if self.enable_voice and not self.listening:
                    self.start_voice_detection()
            elif key == ord('v'):
                # Toggle voice detection
                if self.enable_voice:
                    if self.listening:
                        self.stop_voice_detection()
                    else:
                        self.start_voice_detection()
            
            # Frame rate limiting for smooth playback
            elapsed = time.time() - loop_start
            sleep_time = max(0, frame_time - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        # Stop voice detection before closing
        if self.enable_voice:
            self.stop_voice_detection()
        
        # Stop voice detection before closing
        if self.enable_voice:
            self.stop_voice_detection()
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = FirebaseFaceDetector(
        similarity_threshold=0.30,
        smoothing_frames=5,
        use_gpu=False,
        detection_size=320,  # Smaller for faster processing
        frame_skip=1,  # Process every other frame for smoother performance
        process_resolution=720,  # Lower resolution for faster processing
        voice_similarity_threshold=0.3,
        enable_voice=True,
        voice_chunk_duration=1.0,  # 1 second chunks for faster real-time response in crowded places
        enable_sms=True,  # Enable SMS notifications
        # SMS credentials can be set in 3 ways:
        # 1. Create sinch_config.txt file with 4 lines (one per line):
        #    YOUR_key_id
        #    YOUR_key_secret
        #    YOUR_project_id
        #    YOUR_Sinch_number
        # 2. Set environment variables: SINCH_KEY_ID, SINCH_KEY_SECRET, SINCH_PROJECT_ID, SINCH_FROM_NUMBER
        # 3. Pass them directly as parameters below:
        # sinch_key_id="YOUR_key_id",
        # sinch_key_secret="YOUR_key_secret",
        # sinch_project_id="YOUR_project_id",
        # sinch_from_number="YOUR_Sinch_number"
    )
    
    # Run with webcam (0) or video file path
    detector.run(video_source=0)

