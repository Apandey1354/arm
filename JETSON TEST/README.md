# Running Detector_example.py on Jetson Nano

This guide will help you set up and run the face and voice detection system on an NVIDIA Jetson Nano.

## 📋 Prerequisites

### Hardware Requirements
- **NVIDIA Jetson Nano** (4GB or 8GB model)
- **MicroSD Card**: 64GB+ (Class 10 or better recommended)
- **Power Supply**: 5V 4A barrel jack power supply (official or compatible)
- **USB Webcam**: Any USB 2.0/3.0 webcam
- **USB Microphone**: (Optional, for voice detection)
- **Ethernet Cable** or **WiFi dongle**: For internet connection
- **HDMI Cable** and **Monitor**: For display (or use SSH)

### Software Requirements
- **JetPack 4.6+** or **JetPack 5.x** (L4T)
- **Python 3.8+** (usually pre-installed with JetPack)
- **Internet Connection**: Required for downloading models and dependencies

---

## 🚀 Installation Steps

### Step 1: Flash JetPack to SD Card

1. Download JetPack from [NVIDIA Developer](https://developer.nvidia.com/embedded/jetpack)
2. Flash the image to your microSD card using [Balena Etcher](https://www.balena.io/etcher/) or similar tool
3. Insert SD card into Jetson Nano and boot

### Step 2: Initial Setup

1. Complete the initial Jetson Nano setup wizard
2. Update system packages:
   ```bash
   sudo apt-get update
   sudo apt-get upgrade -y
   ```

### Step 3: Install System Dependencies

```bash
# Install Python and pip (if not already installed)
sudo apt-get install python3-pip python3-dev -y

# Install OpenCV dependencies
sudo apt-get install libopencv-dev python3-opencv -y

# Install audio libraries (for voice detection)
sudo apt-get install portaudio19-dev python3-pyaudio -y
sudo apt-get install libsndfile1 -y

# Install scientific computing libraries
sudo apt-get install libatlas-base-dev libblas-dev liblapack-dev -y

# Install other required system libraries
sudo apt-get install build-essential cmake git -y
```

### Step 4: Navigate to Project Directory

```bash
# Navigate to the JETSON TEST directory
cd "JETSON TEST"
# Or if you're in the project root:
cd "JETSON TEST"
```

### Step 5: Install Python Dependencies

```bash
# Install requirements from backend directory
pip3 install -r ../backend/requirements.txt
```

**Note**: Installation may take 15-30 minutes on Jetson Nano. Some packages (like InsightFace, ONNX Runtime) may take longer to compile/install on ARM architecture.

**If you encounter issues**, try installing packages individually:
```bash
pip3 install opencv-python numpy
pip3 install insightface onnxruntime
pip3 install firebase-admin
pip3 install resemblyzer sounddevice scipy
pip3 install python-dotenv sinch-python-sdk requests
```

### Step 6: Configure Firebase Credentials

You need Firebase credentials to connect to Firestore database.

**Option A: Service Account Key File (Recommended)**

1. Download `serviceAccountKey.json` from Firebase Console
2. Place it in the `backend/` directory (one level up from JETSON TEST)
3. The code will automatically find it at `backend/serviceAccountKey.json`

**Option B: Environment Variable**

Create a `.env` file in the project root:
```bash
# From JETSON TEST directory, go to parent
cd ..
nano .env
```

Add this line (keep JSON on ONE line):
```env
FIREBASE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}'
```

### Step 7: Configure SMS (Optional)

If you want SMS notifications, configure Sinch credentials:

**Option A: Environment Variables**

Add to `.env` file:
```env
SINCH_KEY_ID=your_key_id_here
SINCH_KEY_SECRET=your_key_secret_here
SINCH_PROJECT_ID=your_project_id_here
SINCH_FROM_NUMBER=your_sinch_phone_number
```

**Option B: Config File**

Create `sinch_config.txt` in project root:
```bash
cd ..
nano sinch_config.txt
```

Add 4 lines (one per line):
```
your_key_id
your_key_secret
your_project_id
your_sinch_phone_number
```

---

## 🏃 Running the Detection System

### Step 1: Enable Maximum Performance Mode

Before running, maximize Jetson Nano performance:

```bash
# Set maximum performance mode
sudo nvpmodel -m 0
sudo jetson_clocks

# Verify (optional - monitor in another terminal)
sudo tegrastats
```

**Note**: `jetson_clocks` sets maximum CPU/GPU frequencies. The fan will run faster.

### Step 2: Run the Detection Script

```bash
# From JETSON TEST directory
cd "JETSON TEST"
python3 Detector_example.py
```

### Step 3: Expected Output

You should see:
```
✅ Firebase credentials loaded from serviceAccountKey.json
✅ Firebase Admin SDK initialized successfully
✅ Firestore client connected
📥 DOWNLOADING EMBEDDINGS FROM FIREBASE...
  ✓ Downloaded face embedding for: Person Name (Doc #1, Face #1)
✅ Loaded X face embeddings into memory
✅ Loaded Y voice embeddings into memory
✅ Sinch SMS client initialized
🎥 STARTING FACE & VOICE DETECTION
```

A window will open showing:
- Real-time video feed from webcam
- Face detection boxes (green for matches, red for unknown)
- FPS counter
- Voice detection status
- Detected person information

---

## ⚙️ Configuration Options

The code is already optimized for Jetson Nano, but you can adjust settings in `Detector_example.py`:

```python
detector = FirebaseFaceDetector(
    similarity_threshold=0.30,      # Face match threshold (lower = more sensitive)
    smoothing_frames=5,              # Temporal smoothing frames
    use_gpu=False,                  # Set to True if you want GPU (may be slower on Nano)
    detection_size=320,             # Face detection size (smaller = faster)
    frame_skip=1,                   # Process every Nth frame (1 = every frame, 2 = every other)
    process_resolution=720,          # Max resolution for processing (480, 720, 1080)
    voice_similarity_threshold=0.3,  # Voice match threshold
    enable_voice=True,              # Enable/disable voice detection
    voice_chunk_duration=1.0,        # Voice chunk duration in seconds
    enable_sms=True                 # Enable/disable SMS notifications
)
```

### Performance Tuning for Jetson Nano

**For Better FPS (Lower Quality)**:
```python
detection_size=256,        # Smaller detection size
process_resolution=480,     # Lower resolution
frame_skip=2,              # Skip more frames
```

**For Better Accuracy (Lower FPS)**:
```python
detection_size=640,        # Larger detection size
process_resolution=1080,    # Higher resolution
frame_skip=0,              # Process all frames
```

---

## 🎮 Controls

While the detection window is open:

- **`q`**: Quit the application
- **`r`**: Reload embeddings from Firebase (useful when new persons are added)
- **`v`**: Toggle voice detection on/off

---

## 📊 Expected Performance

### Jetson Nano (4GB) Performance

- **Face Detection FPS**: 5-15 FPS (depending on resolution and settings)
- **Voice Processing**: Real-time (runs in separate thread)
- **Memory Usage**: ~2-3GB RAM
- **CPU Usage**: 60-90% (all cores)
- **Temperature**: 50-70°C (with active cooling)

### Performance Tips

1. **Use Active Cooling**: Jetson Nano can throttle if it gets too hot. Use a fan or heatsink.
2. **Close Other Applications**: Free up memory and CPU for detection.
3. **Lower Resolution**: Use `process_resolution=480` for better FPS.
4. **Frame Skipping**: Use `frame_skip=2` to process every other frame.

---

## 🐛 Troubleshooting

### Issue: Camera Not Detected

**Symptoms**: Error "Could not open video source: 0"

**Solutions**:
```bash
# Check if camera is detected
lsusb
# You should see your webcam listed

# Test camera with v4l2
v4l2-ctl --list-devices

# Try different camera index
# Edit Detector_example.py, change: detector.run(video_source=1)
```

### Issue: Models Not Downloading

**Symptoms**: Long wait time or errors during first run

**Solutions**:
- Ensure internet connection is active
- Models download automatically on first run (InsightFace buffalo_l model)
- Check disk space: `df -h` (need at least 500MB free)
- Models are cached in `~/.insightface/models/` after first download

### Issue: Low FPS (< 5 FPS)

**Solutions**:
1. Reduce resolution:
   ```python
   process_resolution=480  # Instead of 720
   ```
2. Increase frame skipping:
   ```python
   frame_skip=2  # Process every other frame
   ```
3. Reduce detection size:
   ```python
   detection_size=256  # Instead of 320
   ```
4. Ensure maximum performance mode:
   ```bash
   sudo nvpmodel -m 0
   sudo jetson_clocks
   ```

### Issue: Out of Memory

**Symptoms**: System freezes or "Killed" message

**Solutions**:
1. Close other applications
2. Reduce settings:
   ```python
   detection_size=256
   process_resolution=480
   ```
3. Disable voice detection temporarily:
   ```python
   enable_voice=False
   ```
4. Check memory usage:
   ```bash
   free -h
   ```

### Issue: Audio Not Working (Voice Detection)

**Symptoms**: "Error in voice detection" or no voice matches

**Solutions**:
```bash
# Check if microphone is detected
arecord -l

# Test microphone
arecord -d 3 test.wav
aplay test.wav

# Install audio dependencies
sudo apt-get install portaudio19-dev python3-pyaudio -y
pip3 install sounddevice --force-reinstall
```

### Issue: Firebase Connection Error

**Symptoms**: "Firebase credentials not found" or connection timeout

**Solutions**:
1. Check credentials file exists:
   ```bash
   ls -la ../backend/serviceAccountKey.json
   ```
2. Verify internet connection:
   ```bash
   ping google.com
   ```
3. Check Firebase project is active in Firebase Console
4. Verify Firestore is enabled in Firebase Console

### Issue: Packages Fail to Install

**Solutions**:
```bash
# Update pip
pip3 install --upgrade pip

# Install packages one by one
pip3 install opencv-python
pip3 install numpy
pip3 install insightface

# If ONNX Runtime fails, try CPU version
pip3 install onnxruntime
```

### Issue: OpenCV GUI Not Working (Headless Mode)

**Symptoms**: "GUI Error" or no window appears

**Solutions**:
```bash
# Install GUI dependencies
sudo apt-get install python3-tk python3-dev python3-opencv -y

# If using SSH, enable X11 forwarding
ssh -X user@jetson-nano-ip

# Or use VNC for remote desktop
sudo apt-get install tigervnc-standalone-server -y
```

---

## 📁 Output Files

The detection system saves detected person images to:

```
detected_persons/
├── PersonName_20240115_143022_abc12345.jpg      # Cropped person image
├── PersonName_20240115_143022_FULL.jpg          # Full frame with annotation
└── PersonName_20240115_143022_INFO.txt          # Person information
```

Images are saved after **10 seconds** of continuous detection.

---

## 🔧 Advanced Configuration

### Running in Background

To run detection in background (no GUI):

```bash
# Edit Detector_example.py to remove cv2.imshow() calls
# Or use nohup
nohup python3 Detector_example.py > detection.log 2>&1 &
```

### Using Different Camera

```python
# In Detector_example.py, change:
detector.run(video_source=1)  # Use camera index 1
# Or use video file:
detector.run(video_source="/path/to/video.mp4")
```

### GPU Acceleration (Experimental)

Jetson Nano has GPU, but CPU is often faster for this workload:

```python
use_gpu=True  # Try this if you want GPU acceleration
```

**Note**: GPU may actually be slower due to memory transfer overhead. Test both.

---

## 📞 Support

If you encounter issues:

1. Check the main project README.md for general troubleshooting
2. Verify all prerequisites are met
3. Check Jetson Nano system logs: `dmesg | tail -50`
4. Monitor system resources: `sudo tegrastats`
5. Review error messages in terminal output

---

## 🎯 Quick Start Checklist

- [ ] JetPack flashed and Jetson Nano booted
- [ ] System packages updated (`sudo apt-get update && upgrade`)
- [ ] System dependencies installed (OpenCV, audio libraries)
- [ ] Python dependencies installed (`pip3 install -r ../backend/requirements.txt`)
- [ ] Firebase credentials configured (`backend/serviceAccountKey.json` or `.env`)
- [ ] SMS credentials configured (optional, `sinch_config.txt` or `.env`)
- [ ] Maximum performance mode enabled (`sudo nvpmodel -m 0 && sudo jetson_clocks`)
- [ ] Camera connected and tested
- [ ] Microphone connected (if using voice detection)
- [ ] Run detection: `python3 Detector_example.py`

---

## 📝 Notes

- **First Run**: Models will download automatically (may take 5-10 minutes)
- **Internet Required**: For Firebase connection and model downloads
- **Performance**: Expect 5-15 FPS on Jetson Nano (optimized for ARM)
- **Memory**: System uses 2-3GB RAM, ensure 4GB+ available
- **Temperature**: Monitor temperature, use active cooling if needed

---

**Built for NVIDIA Jetson Nano - ARM AI Challenge**

