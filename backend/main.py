from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import firebase_admin
from firebase_admin import credentials, firestore
import os
import base64
from datetime import datetime
from dotenv import load_dotenv
from image_processor import extract_embedding
from audio_processor import extract_voice_embedding

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="FindMe Backend API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = None
    
    # Check if using service account key file
    if os.path.exists("serviceAccountKey.json"):
        try:
            cred = credentials.Certificate("serviceAccountKey.json")
            print("✅ Firebase credentials loaded from serviceAccountKey.json")
        except Exception as e:
            print(f"❌ Error loading serviceAccountKey.json: {e}")
    
    # Check if using environment variable
    elif os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"):
        try:
            import json
            service_account_info = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"))
            cred = credentials.Certificate(service_account_info)
            print("✅ Firebase credentials loaded from environment variable")
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing FIREBASE_SERVICE_ACCOUNT_KEY: Invalid JSON - {e}")
        except Exception as e:
            print(f"❌ Error loading credentials from environment variable: {e}")
    
    # If no credentials found, show helpful error
    if cred is None:
        print("\n" + "="*60)
        print("❌ FIREBASE CREDENTIALS NOT FOUND!")
        print("="*60)
        print("\nPlease set up Firebase credentials using ONE of these methods:\n")
        print("METHOD 1: JSON File (Recommended for development)")
        print("  1. Download service account key from Firebase Console")
        print("  2. Save it as 'serviceAccountKey.json' in the backend folder")
        print("  3. Restart the server\n")
        print("METHOD 2: Environment Variable")
        print("  1. Create a .env file in the backend folder")
        print("  2. Add: FIREBASE_SERVICE_ACCOUNT_KEY='{your-json-here}'")
        print("  3. Make sure python-dotenv is installed: pip install python-dotenv")
        print("  4. Restart the server\n")
        print("For detailed instructions, see: backend/FIREBASE_SETUP.md")
        print("="*60 + "\n")
        raise Exception(
            "Firebase credentials not configured. "
            "Please set up serviceAccountKey.json or FIREBASE_SERVICE_ACCOUNT_KEY environment variable. "
            "See backend/FIREBASE_SETUP.md for instructions."
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
except Exception as e:
    print(f"❌ Error connecting to Firestore: {e}")
    raise

@app.get("/")
async def root():
    return {"message": "FindMe Backend API is running"}

@app.post("/api/upload")
async def upload_missing_person(
    fullName: str = Form(...),
    age: str = Form(...),
    cityLastSeen: str = Form(...),
    dateLastSeen: str = Form(...),
    contactPhone: str = Form(...),
    nearbyPoliceStation: str = Form(...),
    additionalDescription: Optional[str] = Form(None),
    images: List[UploadFile] = File(...),
    audio: Optional[UploadFile] = File(None)
):
    """
    Endpoint to receive missing person upload data and images.
    Processes images to extract face embeddings and stores everything in Firebase.
    """
    try:
        if not images or len(images) == 0:
            raise HTTPException(status_code=400, detail="At least one image is required")
        
        # Process all images and extract embeddings
        processed_images = []
        embeddings = []
        image_base64_list = []
        
        for idx, image in enumerate(images):
            # Read image data
            image_data = await image.read()
            
            # Convert image to base64 for storage
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image_base64_list.append(image_base64)
            
            # Process image and extract embedding
            embedding = extract_embedding(image_data)
            
            if embedding is None:
                # If no face detected, still store the image but without embedding
                processed_images.append({
                    "index": idx,
                    "filename": image.filename or f"image_{idx}.jpg",
                    "has_face": False,
                    "embedding": None
                })
            else:
                # Convert numpy array to list for JSON serialization
                embedding_list = embedding.tolist()
                embeddings.append(embedding_list)
                
                processed_images.append({
                    "index": idx,
                    "filename": image.filename or f"image_{idx}.jpg",
                    "has_face": True,
                    "embedding": embedding_list
                })
        
        # Process audio if provided
        audio_embedding = None
        audio_base64 = None
        audio_metadata = None
        
        if audio:
            try:
                audio_data = await audio.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                # Extract voice embedding
                audio_embedding = extract_voice_embedding(audio_data)
                
                if audio_embedding is not None:
                    audio_metadata = {
                        "filename": audio.filename or "audio.wav",
                        "has_voice": True,
                        "embedding": audio_embedding.tolist()
                    }
                else:
                    audio_metadata = {
                        "filename": audio.filename or "audio.wav",
                        "has_voice": False,
                        "embedding": None
                    }
            except Exception as e:
                print(f"Error processing audio: {str(e)}")
                audio_metadata = {
                    "filename": audio.filename or "audio.wav",
                    "has_voice": False,
                    "embedding": None
                }
        
        # Create document data
        upload_data = {
            "fullName": fullName,
            "age": int(age),
            "cityLastSeen": cityLastSeen,
            "dateLastSeen": dateLastSeen,
            "contactPhone": contactPhone,
            "nearbyPoliceStation": nearbyPoliceStation,
            "additionalDescription": additionalDescription or "",
            "images": image_base64_list,  # Store base64 encoded images
            "imageMetadata": processed_images,  # Store metadata with embeddings (embeddings are stored here per image)
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "status": "pending"
        }
        
        # Add audio data if provided
        if audio:
            upload_data["audio"] = audio_base64
            upload_data["audioMetadata"] = audio_metadata
        
        # Save to Firebase "upload" collection
        doc_ref = db.collection("upload").add(upload_data)
        
        response_data = {
            "success": True,
            "message": "Upload successful",
            "documentId": doc_ref[1].id,
            "imagesProcessed": len(processed_images),
            "facesDetected": len(embeddings)
        }
        
        if audio:
            response_data["audioProcessed"] = True
            response_data["voiceDetected"] = audio_embedding is not None
        
        return response_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing upload: {str(e)}")

@app.post("/api/counselor")
async def submit_counselor_request(
    name: str = Form(...),
    phone: str = Form(...),
    message: str = Form(...)
):
    """
    Endpoint to receive counselor callback requests.
    Stores data in Firebase "counselor" collection.
    """
    try:
        # Create document data
        counselor_data = {
            "name": name,
            "phone": phone,
            "message": message,
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "status": "pending"
        }
        
        # Save to Firebase "counselor" collection
        doc_ref = db.collection("counselor").add(counselor_data)
        
        return {
            "success": True,
            "message": "Counselor request submitted successfully",
            "documentId": doc_ref[1].id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting counselor request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

