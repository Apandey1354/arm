"""
Audio processing module for voice embedding extraction using resemblyzer.
"""
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.io.wavfile import write
import io
import tempfile
import os
from typing import Optional

# Initialize the voice encoder
# This will be initialized once when the module is imported
encoder = None

def initialize_voice_encoder():
    """Initialize the voice encoder."""
    global encoder
    if encoder is None:
        encoder = VoiceEncoder()
    return encoder

def extract_voice_embedding(audio_data: bytes, sample_rate: int = 16000) -> Optional[np.ndarray]:
    """
    Extract voice embedding from audio data.
    
    Args:
        audio_data: Audio data as bytes (supports WAV, MP3, M4A, etc.)
        sample_rate: Sample rate of the audio (default: 16000)
        
    Returns:
        Voice embedding as numpy array, or None if processing fails
    """
    try:
        # Initialize voice encoder if not already done
        if encoder is None:
            initialize_voice_encoder()
        
        # Create a temporary file to save the audio
        # Use .wav extension but resemblyzer can handle various formats
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_path = temp_file.name
            try:
                # Write audio data to temporary file
                temp_file.write(audio_data)
                temp_file.flush()
                
                # Preprocess the audio file (resemblyzer handles format conversion)
                # preprocess_wav can handle WAV, MP3, M4A, FLAC, etc.
                wav = preprocess_wav(temp_path)
                
                # Extract embedding
                embedding = encoder.embed_utterance(wav)
                
                return embedding
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
    
    except Exception as e:
        print(f"Error extracting voice embedding: {str(e)}")
        return None

def process_audio(audio_data: bytes, sample_rate: int = 16000) -> dict:
    """
    Process an audio file and return metadata.
    
    Args:
        audio_data: Audio data as bytes
        sample_rate: Sample rate of the audio
        
    Returns:
        Dictionary with processing results
    """
    embedding = extract_voice_embedding(audio_data, sample_rate)
    
    return {
        "has_voice": embedding is not None,
        "embedding": embedding.tolist() if embedding is not None else None
    }

# Initialize on module import
initialize_voice_encoder()

