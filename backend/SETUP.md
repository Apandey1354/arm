# Backend Setup Guide

## Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Firebase:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Select your project (or create a new one)
   - Go to Project Settings → Service Accounts
   - Click "Generate new private key"
   - Save the downloaded JSON file as `serviceAccountKey.json` in the `backend` directory
   - Enable Firestore Database in your Firebase project

3. **Run the server:**
   ```bash
   python main.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Verify it's working:**
   - Open `http://localhost:8000` in your browser
   - You should see: `{"message":"FindMe Backend API is running"}`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### InsightFace Model Download
On first run, InsightFace will automatically download the `buffalo_l` model. This may take a few minutes and requires an internet connection.

### Firebase Authentication
If you get Firebase authentication errors:
- Make sure `serviceAccountKey.json` is in the backend directory
- Verify the service account has Firestore permissions
- Check that Firestore is enabled in your Firebase project

### Port Already in Use
If port 8000 is already in use, change it in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change port number
```

### GPU Support (Optional)
For faster processing with GPU:
1. Install CUDA and cuDNN
2. Install `onnxruntime-gpu` instead of `onnxruntime`
3. In `image_processor.py`, change `ctx_id=0` to `ctx_id=-1`

## Environment Variables (Optional)

You can use environment variables instead of the JSON file:

```bash
export FIREBASE_SERVICE_ACCOUNT_KEY='{"type":"service_account",...}'
```

## Testing the API

### Test Upload Endpoint:
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "fullName=John Doe" \
  -F "age=25" \
  -F "cityLastSeen=New York" \
  -F "dateLastSeen=2024-01-15" \
  -F "contactPhone=1234567890" \
  -F "images=@/path/to/image.jpg"
```

### Test Counselor Endpoint:
```bash
curl -X POST "http://localhost:8000/api/counselor" \
  -F "name=Jane Smith" \
  -F "phone=9876543210" \
  -F "message=I need help"
```





