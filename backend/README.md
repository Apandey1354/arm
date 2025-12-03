# Backend

This is the backend implementation for the FindMe platform using FastAPI, Firebase, and InsightFace.

## Features

- **Image Processing**: Extracts face embeddings from uploaded images using InsightFace
- **Firebase Integration**: Stores data in two collections:
  - `upload`: Missing person reports with images and embeddings
  - `counselor`: Counselor callback requests
- **RESTful API**: FastAPI endpoints for data submission

## Setup

### Prerequisites

- Python 3.8 or higher
- Firebase project with Firestore enabled
- Firebase service account key

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Firebase:
   - Go to Firebase Console → Project Settings → Service Accounts
   - Generate a new private key
   - Save it as `serviceAccountKey.json` in the backend directory
   - **OR** set the `FIREBASE_SERVICE_ACCOUNT_KEY` environment variable with the JSON content

3. Download InsightFace models:
   The models will be automatically downloaded on first run. Make sure you have internet connection.

### Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST `/api/upload`
Upload missing person information with images.

**Form Data:**
- `fullName` (string, required)
- `age` (string, required)
- `cityLastSeen` (string, required)
- `dateLastSeen` (string, required)
- `contactPhone` (string, required)
- `additionalDescription` (string, optional)
- `images` (files, required, multiple)

**Response:**
```json
{
  "success": true,
  "message": "Upload successful",
  "documentId": "abc123",
  "imagesProcessed": 3,
  "facesDetected": 2
}
```

### POST `/api/counselor`
Submit counselor callback request.

**Form Data:**
- `name` (string, required)
- `phone` (string, required)
- `message` (string, required)

**Response:**
```json
{
  "success": true,
  "message": "Counselor request submitted successfully",
  "documentId": "xyz789"
}
```

## Firebase Collections

### `upload` Collection
Documents contain:
- Personal information (fullName, age, cityLastSeen, dateLastSeen, contactPhone)
- Images (base64 encoded)
- Face embeddings (numpy arrays converted to lists)
- Metadata (timestamps, status)

### `counselor` Collection
Documents contain:
- Contact information (name, phone, message)
- Metadata (timestamps, status)

## Notes

- Images are stored as base64 strings in Firestore. For production, consider using Firebase Storage instead.
- Face embeddings are 512-dimensional vectors (for buffalo_l model).
- If no face is detected in an image, the image is still stored but without an embedding.
- The InsightFace model uses CPU by default. For GPU support, install `onnxruntime-gpu` and set `ctx_id=-1` in `image_processor.py`.
