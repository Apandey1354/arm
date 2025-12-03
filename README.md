# FindMe - Missing Person Detection & Human Trafficking Prevention Platform

<div align="center">

**⚠️ Hackathon Submission - ARM AI Challenge**

An AI-powered platform for real-time missing person detection, human trafficking prevention, and identification through advanced facial and voice recognition.

[![Next.js](https://img.shields.io/badge/Next.js-14.2.5-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![InsightFace](https://img.shields.io/badge/InsightFace-0.7.3-orange)](https://github.com/deepinsight/insightface)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-FFCA28)](https://firebase.google.com/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Jetson Nano Setup](#jetson-nano-setup)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

FindMe is a comprehensive platform designed to help locate missing persons and prevent human trafficking through:

- **Real-time Face Recognition**: Advanced AI-powered facial recognition using InsightFace
- **Voice Identification**: Multi-speaker voice recognition using Resemblyzer
- **SMS Notifications**: Automatic alerts with location data via Sinch API
- **Web Interface**: User-friendly Next.js frontend for reporting missing persons
- **Cloud Storage**: Secure Firebase Firestore database for person data
- **Edge Computing**: Optimized for ARM-based devices like Jetson Nano

---

## ✨ Features

### Frontend Features
- 📝 Missing person reporting form with image/audio upload
- 🖼️ Multi-image upload (up to 10 images, 5MB each)
- 🎤 Voice sample upload for identification
- 📍 Police station coordination
- 💬 Consultation page
- 📱 Responsive design with modern UI
- ✅ Form validation and error handling

### Backend Features
- 🔐 RESTful API with FastAPI
- 🧠 Face embedding extraction (512-dimensional)
- 🎙️ Voice embedding extraction (256-dimensional)
- ☁️ Firebase Firestore integration
- 📦 Base64 image storage
- 🔄 Automatic model initialization

### Detection System Features
- 🎥 Real-time video processing (webcam or video file)
- 👤 Multi-face detection and recognition
- 🔊 Real-time voice detection (separate thread)
- 📊 Temporal smoothing for stable results
- 💾 Automatic image saving after 10 seconds of detection
- 📱 SMS notifications with GPS coordinates
- ⏱️ 1-hour SMS cooldown per person
- 🎮 Keyboard controls (q=quit, r=reload, v=toggle voice)

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   Frontend      │  Next.js 14 (React 18, TypeScript)
│   (Port 3000)   │  └─> Upload Form, Consultation, Home Page
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Backend API   │  FastAPI (Python)
│   (Port 8000)   │  └─> Image/Audio Processing, Firebase Integration
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Firebase      │  Firestore Database
│   Cloud         │  └─> Person Data, Embeddings, Images
└─────────────────┘

┌─────────────────┐
│ Detection System│  Python (Detector_example.py)
│   (Standalone)  │  └─> Real-time Face/Voice Detection
│                 │      └─> SMS Notifications (Sinch)
└─────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14.2.5 (App Router)
- **Language**: TypeScript 5.5.4
- **UI Library**: React 18.3.1
- **Styling**: Tailwind CSS 3.4.7
- **Animations**: Framer Motion 11.3.3
- **Forms**: React Hook Form 7.52.1 + Zod 3.23.8
- **Icons**: Lucide React 0.424.0
- **UI Components**: Radix UI

### Backend
- **Framework**: FastAPI 0.115.0
- **Server**: Uvicorn 0.30.6
- **Language**: Python 3.8+

### AI/ML Models
- **Face Recognition**: InsightFace (buffalo_l model)
  - Embedding dimension: 512
  - Framework: ONNX Runtime 1.19.1
  - Similarity threshold: 0.30-0.35
  
- **Voice Recognition**: Resemblyzer
  - Embedding dimension: 256
  - Sample rate: 16000 Hz
  - Similarity threshold: 0.3

### Database & Storage
- **Database**: Firebase Firestore
- **Storage**: Base64 encoded images in Firestore

### External Services
- **SMS**: Sinch API (sinch-python-sdk 2.0.0)
- **Geolocation**: IP-API (ip-api.com)

### Computer Vision
- **Library**: OpenCV 4.10.0.84
- **Processing**: NumPy 1.26.4

---

## 📦 Prerequisites

### For Frontend
- Node.js 18.x or higher
- npm 9.x or higher

### For Backend
- Python 3.8 or higher
- pip (Python package manager)

### For Detection System
- Python 3.8 or higher
- USB Webcam or video file
- (Optional) CUDA-capable GPU for faster processing

### For Jetson Nano
- NVIDIA Jetson Nano with JetPack 4.6+ or JetPack 5.x
- MicroSD card (64GB+ recommended)
- Power supply (5V 4A)
- USB webcam

### Services Required
- Firebase project with Firestore enabled
- Sinch account (for SMS notifications)
- Internet connection

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "FINDME"
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

This will install all frontend dependencies including:
- Next.js, React, TypeScript
- Tailwind CSS and styling libraries
- Form handling and validation libraries
- UI components

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn
- Firebase Admin SDK
- InsightFace and ONNX Runtime
- OpenCV and NumPy
- Resemblyzer for voice recognition
- Sinch SDK for SMS
- Other dependencies

### 4. Detection System Setup

The detection system uses the same dependencies as the backend:

```bash
# From project root
pip install -r backend/requirements.txt
```

**Note**: For Jetson Nano, see [Jetson Nano Setup](#jetson-nano-setup) section below.

---

## ⚙️ Configuration

### 1. Firebase Configuration

You need Firebase credentials to store and retrieve person data.

**Option A: Service Account Key File (Recommended for Development)**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project → ⚙️ Settings → Project settings
3. Go to "Service accounts" tab
4. Click "Generate new private key"
5. Download the JSON file
6. Rename it to `serviceAccountKey.json`
7. Place it in the `backend/` directory

**Option B: Environment Variable (Recommended for Production)**

1. Download the service account key (same as Option A)
2. Copy the entire JSON content
3. Create a `.env` file in `backend/` directory:
   ```env
   FIREBASE_SERVICE_ACCOUNT_KEY='{"type":"service_account",...}'
   ```
   (Keep it on ONE line, wrap in single quotes)

### 2. Sinch SMS Configuration

For SMS notifications, configure Sinch credentials:

**Option A: Environment Variables**

Create `.env` file in root or `backend/` directory:

```env
SINCH_KEY_ID=your_key_id_here
SINCH_KEY_SECRET=your_key_secret_here
SINCH_PROJECT_ID=your_project_id_here
SINCH_FROM_NUMBER=your_sinch_phone_number
```

**Option B: Config File**

Create `sinch_config.txt` in project root:

```
your_key_id
your_key_secret
your_project_id
your_sinch_phone_number
```

**Option C: Direct Parameters**

Pass credentials directly in `Detector_example.py` (see code comments).

### 3. Frontend API Configuration

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🏃 Running the Project

### Step 1: Start Backend Server

```bash
cd backend
python main.py
```

Or with uvicorn directly:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will start on `http://localhost:8000`

**Expected Output:**
```
✅ Firebase credentials loaded from serviceAccountKey.json
✅ Firebase Admin SDK initialized successfully
✅ Firestore client connected
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

**Expected Output:**
```
  ▲ Next.js 14.2.5
  - Local:        http://localhost:3000
  - ready started server on 0.0.0.0:3000
```

### Step 3: Run Detection System

**For Regular PC/Laptop:**

```bash
# From project root
python Detector_example.py
```

**For Jetson Nano:**

See [Jetson Nano Setup](#jetson-nano-setup) section below.

**Expected Output:**
```
✅ Firebase credentials loaded from serviceAccountKey.json
✅ Firebase Admin SDK initialized successfully
✅ Firestore client connected
📥 DOWNLOADING EMBEDDINGS FROM FIREBASE...
✅ Loaded X face embeddings into memory
✅ Loaded Y voice embeddings into memory
✅ Sinch SMS client initialized
🎥 STARTING FACE & VOICE DETECTION
```

### Step 4: Access the Application

1. **Web Interface**: Open `http://localhost:3000` in your browser
2. **Upload Missing Person**: Go to Upload page and fill the form
3. **Detection Window**: The detection system will show a window with real-time face/voice detection

---

## 🤖 Jetson Nano Setup

The `Detector_example.py` is specifically optimized for running on NVIDIA Jetson Nano (ARM-based edge device).

### Prerequisites for Jetson Nano

1. **Flash JetPack** (4.6+ or 5.x) to microSD card
2. **Boot Jetson Nano** and complete initial setup
3. **Update system packages**:
   ```bash
   sudo apt-get update
   sudo apt-get upgrade -y
   ```

### Installation on Jetson Nano

#### 1. Install System Dependencies

```bash
# Install Python and pip
sudo apt-get install python3-pip python3-dev -y

# Install OpenCV dependencies
sudo apt-get install libopencv-dev python3-opencv -y

# Install audio libraries
sudo apt-get install portaudio19-dev python3-pyaudio -y
sudo apt-get install libsndfile1 -y

# Install other system libraries
sudo apt-get install libatlas-base-dev libblas-dev liblapack-dev -y
```

#### 2. Install Python Dependencies

```bash
# Navigate to project directory
cd "FINDME"

# Install requirements
pip3 install -r backend/requirements.txt
```

**Note**: Some packages may take longer to install on ARM. Be patient.

#### 3. Configure for Jetson Nano

The `Detector_example.py` is already configured for ARM/CPU execution:

```python
# In Detector_example.py (already set)
use_gpu=False  # Jetson Nano uses CPU (or enable GPU if needed)
detection_size=320  # Smaller for ARM performance
process_resolution=720  # Reduced resolution
frame_skip=1  # Process every other frame
```

#### 4. Run on Jetson Nano

```bash
# From project root
python3 Detector_example.py
```

### Jetson Nano Performance Tips

1. **Enable Maximum Performance Mode**:
   ```bash
   sudo nvpmodel -m 0
   sudo jetson_clocks
   ```

2. **Monitor Performance**:
   ```bash
   # In another terminal
   sudo tegrastats
   ```

3. **Expected Performance**:
   - Face Detection: 5-15 FPS (depending on resolution)
   - Voice Processing: Real-time (separate thread)
   - Memory Usage: ~2-3GB RAM

4. **Optimization Settings** (already in code):
   - Lower resolution (720p instead of 1080p)
   - Frame skipping (process every other frame)
   - Smaller detection size (320x320)
   - CPU execution (no GPU overhead)

### Jetson Nano Troubleshooting

**Issue**: Models take too long to load
- **Solution**: Models are downloaded on first run. Subsequent runs are faster.

**Issue**: Low FPS
- **Solution**: Reduce `process_resolution` to 480, increase `frame_skip` to 2

**Issue**: Out of memory
- **Solution**: Close other applications, reduce `detection_size` to 256

**Issue**: Audio not working
- **Solution**: Check USB microphone connection, install `portaudio19-dev`

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```
GET /
```
**Response:**
```json
{
  "message": "FindMe Backend API is running"
}
```

#### 2. Upload Missing Person
```
POST /api/upload
Content-Type: multipart/form-data
```

**Request Parameters:**
- `fullName` (string, required): Full name of missing person
- `age` (string, required): Age of missing person
- `cityLastSeen` (string, required): City where person was last seen
- `dateLastSeen` (string, required): Date when person was last seen (YYYY-MM-DD)
- `contactPhone` (string, required): Contact phone number
- `nearbyPoliceStation` (string, required): Police station name and address
- `additionalDescription` (string, optional): Additional information
- `images` (File[], required): Image files (max 10, 5MB each)
- `audio` (File, optional): Audio file (10MB max)

**Response:**
```json
{
  "message": "Data uploaded successfully",
  "docId": "document_id_in_firebase",
  "imagesProcessed": 3,
  "facesDetected": 2,
  "audioProcessed": true,
  "voiceDetected": true
}
```

**Error Responses:**
- `400`: Bad request (missing images, invalid data)
- `500`: Server error

---

## 📁 Project Structure

```
FINDME/
├── frontend/                 # Next.js frontend application
│   ├── app/
│   │   ├── page.tsx         # Home page
│   │   ├── upload/
│   │   │   └── page.tsx     # Upload form
│   │   ├── consultation/
│   │   │   └── page.tsx     # Consultation page
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   ├── Navbar.tsx       # Navigation component
│   │   └── ui/              # Reusable UI components
│   ├── lib/
│   │   ├── api.ts           # API configuration
│   │   └── utils.ts         # Utility functions
│   ├── package.json         # Frontend dependencies
│   └── next.config.js       # Next.js configuration
│
├── backend/                  # FastAPI backend
│   ├── main.py              # FastAPI application
│   ├── image_processor.py   # Face embedding extraction
│   ├── audio_processor.py   # Voice embedding extraction
│   ├── requirements.txt     # Python dependencies
│   ├── serviceAccountKey.json  # Firebase credentials (optional)
│   └── .env                 # Environment variables (optional)
│
├── Detector_example.py       # Real-time detection system (for Jetson Nano)
│
├── detected_persons/         # Saved detection images
│   ├── {name}_{timestamp}_{key}.jpg
│   ├── {name}_{timestamp}_FULL.jpg
│   └── {name}_{timestamp}_INFO.txt
│
├── TECHNICAL_DOCUMENTATION.txt  # Detailed technical docs
│
└── README.md                 # This file
```

---

## 🔬 Technical Details

### Face Recognition Pipeline

1. **Image Upload** → Backend receives image
2. **Face Detection** → InsightFace detects faces
3. **Embedding Extraction** → 512-dim vector extracted
4. **Storage** → Embedding saved to Firebase
5. **Real-time Matching** → Detection system compares live video with stored embeddings
6. **Similarity Calculation** → Cosine similarity (threshold: 0.30)
7. **Temporal Smoothing** → Average over 5 frames
8. **Match Decision** → If similarity > threshold, person identified

### Voice Recognition Pipeline

1. **Audio Upload** → Backend receives audio file
2. **Preprocessing** → Convert to WAV, resample to 16kHz
3. **Embedding Extraction** → 256-dim vector extracted
4. **Storage** → Embedding saved to Firebase
5. **Real-time Matching** → Detection system records 1-second chunks
6. **Similarity Calculation** → Cosine similarity (threshold: 0.3)
7. **Multi-speaker Detection** → Finds all matches above threshold
8. **Active Speaker Tracking** → Tracks currently speaking persons

### SMS Notification Flow

1. **Person Detected** → First time detection triggers SMS check
2. **Cooldown Check** → Verify 1 hour has passed since last SMS
3. **Location Retrieval** → Get GPS coordinates via IP geolocation
4. **Message Formatting** → Format: Name, Age, Coordinates
5. **SMS Sending** → Send via Sinch API
6. **Cooldown Update** → Record SMS send time

### Data Storage Schema

**Firebase Firestore Collection: `upload`**

```json
{
  "fullName": "John Doe",
  "age": 25,
  "cityLastSeen": "New York",
  "dateLastSeen": "2024-01-15",
  "contactPhone": "+1234567890",
  "nearbyPoliceStation": "NYPD Station 123 Main St",
  "additionalDescription": "Last seen wearing blue jacket",
  "images": ["base64_encoded_image1", "base64_encoded_image2"],
  "imageMetadata": [
    {
      "index": 0,
      "filename": "image1.jpg",
      "has_face": true,
      "embedding": [0.123, 0.456, ...]  // 512 dimensions
    }
  ],
  "audioMetadata": {
    "filename": "audio.wav",
    "has_voice": true,
    "embedding": [0.789, 0.012, ...]  // 256 dimensions
  },
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

---

## 🐛 Troubleshooting

### Frontend Issues

**Issue**: `npm install` fails
- **Solution**: Clear cache: `npm cache clean --force`, then retry

**Issue**: Port 3000 already in use
- **Solution**: Change port: `npm run dev -- -p 3001`

**Issue**: API connection error
- **Solution**: Ensure backend is running on port 8000

### Backend Issues

**Issue**: Firebase credentials not found
- **Solution**: Check `backend/serviceAccountKey.json` exists or set `FIREBASE_SERVICE_ACCOUNT_KEY` in `.env`

**Issue**: Models not downloading
- **Solution**: Check internet connection. Models download automatically on first use.

**Issue**: Port 8000 already in use
- **Solution**: Change port in `main.py` or use: `uvicorn main:app --port 8001`

### Detection System Issues

**Issue**: Camera not detected
- **Solution**: Check USB connection, try different camera, or use video file path

**Issue**: SMS not sending
- **Solution**: Check Sinch credentials in `.env` or `sinch_config.txt`

**Issue**: Low FPS
- **Solution**: Reduce `process_resolution`, increase `frame_skip`, or enable GPU

**Issue**: Out of memory
- **Solution**: Reduce `detection_size`, close other applications

### Jetson Nano Specific Issues

**Issue**: Packages fail to install
- **Solution**: Use `pip3` instead of `pip`, install system dependencies first

**Issue**: OpenCV not working
- **Solution**: Install system OpenCV: `sudo apt-get install python3-opencv`

**Issue**: Audio not recording
- **Solution**: Install `portaudio19-dev` and `python3-pyaudio`

---

## 📝 Usage Examples

### Upload Missing Person via Web Interface

1. Navigate to `http://localhost:3000/upload`
2. Fill in all required fields:
   - Full Name
   - Age
   - City Last Seen
   - Date Last Seen
   - Contact Phone
   - Nearby Police Station
3. Upload at least one image (up to 10 images)
4. (Optional) Upload audio file
5. Click "Submit Information"
6. Wait for confirmation message

### Run Detection System

```bash
# Basic usage (webcam)
python Detector_example.py

# With video file
# Edit Detector_example.py, change: detector.run(video_source="path/to/video.mp4")
```

### Keyboard Controls (Detection System)

- **`q`**: Quit application
- **`r`**: Reload embeddings from Firebase
- **`v`**: Toggle voice detection on/off

---

## 🔒 Security Notes

- **Firebase Credentials**: Never commit `serviceAccountKey.json` to version control
- **Sinch Credentials**: Store in environment variables, not in code
- **API Endpoints**: Add authentication for production deployment
- **HTTPS**: Use HTTPS in production for secure data transmission
- **Input Validation**: All inputs are validated on both frontend and backend

---

## 📊 Performance Metrics

### Expected Performance (Desktop/Laptop)
- Face Detection: 15-30 FPS (CPU), 30-60 FPS (GPU)
- Voice Processing: Real-time (separate thread)
- Memory Usage: 2-4GB RAM

### Expected Performance (Jetson Nano)
- Face Detection: 5-15 FPS (CPU)
- Voice Processing: Real-time
- Memory Usage: 2-3GB RAM

---

## 🚧 Known Limitations

1. Face detection requires clear face visibility
2. Voice detection requires clear audio (no background noise)
3. SMS requires valid phone numbers with country code
4. Location accuracy depends on IP geolocation (not GPS)
5. Performance varies by hardware specifications
6. Models require internet connection for first-time download

---

## 🔮 Future Enhancements

- [ ] GPU acceleration support for Jetson Nano
- [ ] Batch processing for multiple videos
- [ ] Cloud deployment (AWS, GCP, Azure)
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Real-time database updates
- [ ] WebSocket for live updates

---

## 📄 License

This project is a hackathon submission for the ARM AI Challenge.

---

## 👥 Contributing

This is a hackathon project. For questions or issues, please refer to the technical documentation.

---

## 📞 Support

For technical support or questions:
1. Check `TECHNICAL_DOCUMENTATION.txt` for detailed information
2. Review troubleshooting section above
3. Check Firebase and Sinch service status

---

## 🙏 Acknowledgments

- **InsightFace**: Face recognition models
- **Resemblyzer**: Voice recognition
- **Firebase**: Cloud database and storage
- **Sinch**: SMS notification service
- **Next.js & FastAPI**: Web frameworks

---

<div align="center">

**Built with ❤️ for the ARM AI Challenge**

⚠️ **Hackathon Submission - ARM AI Challenge**

</div>
