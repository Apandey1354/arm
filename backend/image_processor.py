"""
Image processing module for face embedding extraction using insightface.
"""
import insightface
from insightface.app import FaceAnalysis
import cv2
import numpy as np
from typing import Optional

# Initialize the face analysis app
# This will be initialized once when the module is imported
app = None

def initialize_face_analysis():
    """Initialize the face analysis app."""
    global app
    if app is None:
        app = FaceAnalysis(name="buffalo_l")
        app.prepare(ctx_id=0)  # Use CPU (ctx_id=0), use ctx_id=-1 for GPU if available
    return app

def extract_embedding(image_data: bytes) -> Optional[np.ndarray]:
    """
    Extract face embedding from image data.
    
    Args:
        image_data: Image data as bytes
        
    Returns:
        Normalized embedding as numpy array, or None if no face detected
    """
    try:
        # Initialize face analysis if not already done
        if app is None:
            initialize_face_analysis()
        
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        
        # Decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return None
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Get faces
        faces = app.get(img_rgb)
        
        if len(faces) == 0:
            return None
        
        # Return normalized embedding of the first face
        return faces[0].normed_embedding
    
    except Exception as e:
        print(f"Error extracting embedding: {str(e)}")
        return None

def process_image(image_data: bytes) -> dict:
    """
    Process an image and return metadata.
    
    Args:
        image_data: Image data as bytes
        
    Returns:
        Dictionary with processing results
    """
    embedding = extract_embedding(image_data)
    
    return {
        "has_face": embedding is not None,
        "embedding": embedding.tolist() if embedding is not None else None
    }

# Initialize on module import
initialize_face_analysis()





