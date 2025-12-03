# Troubleshooting Guide

## "Failed to fetch" Error

This error means the frontend cannot connect to the backend. Here's how to fix it:

### Step 1: Check if Backend is Running

1. Open a terminal/command prompt
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Start the backend server:
   ```bash
   python main.py
   ```
   
   You should see:
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

4. **Keep this terminal open** - the server needs to keep running!

### Step 2: Verify Backend is Accessible

Open your browser and go to: `http://localhost:8000`

You should see:
```json
{"message":"FindMe Backend API is running"}
```

If you see this, the backend is working! ✅

### Step 3: Check Frontend is Running

1. Open a **new** terminal/command prompt
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Start the frontend:
   ```bash
   npm run dev
   ```
   
   You should see:
   ```
   ▲ Next.js 14.2.5
   - Local:        http://localhost:3000
   ```

### Step 4: Check Port Numbers

- **Backend** should be running on: `http://localhost:8000`
- **Frontend** should be running on: `http://localhost:3000`

If your frontend runs on a different port, update the CORS settings in `backend/main.py`

### Step 5: Check Browser Console

1. Open your browser's Developer Tools (F12)
2. Go to the **Console** tab
3. Try submitting the form again
4. Look for any error messages

Common errors:
- `Failed to fetch` = Backend not running or wrong URL
- `CORS error` = Backend CORS not configured correctly
- `Network error` = Firewall or network issue

## Common Issues

### Issue: "Module not found" when starting backend

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"

**Solution:**
1. Find what's using port 8000:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```
2. Kill the process or change the port in `backend/main.py`

### Issue: Firebase connection error

**Solution:**
1. Make sure you have `serviceAccountKey.json` in the backend folder OR
2. Set up the `.env` file with `FIREBASE_SERVICE_ACCOUNT_KEY`
3. Check the Firebase setup guide: `backend/FIREBASE_SETUP.md`

### Issue: CORS errors in browser console

**Solution:**
1. Check that your frontend URL is in the CORS allow list in `backend/main.py`
2. Make sure both servers are running
3. Try accessing the frontend via `http://localhost:3000` (not `127.0.0.1`)

### Issue: Images not uploading

**Solution:**
1. Check backend logs for errors
2. Make sure images are valid (JPG, PNG, etc.)
3. Check file size (should be under 5MB)
4. Verify InsightFace models are downloaded (first run takes time)

## Testing the Connection

### Test 1: Backend Health Check
```bash
curl http://localhost:8000
```
Should return: `{"message":"FindMe Backend API is running"}`

### Test 2: Test Upload Endpoint
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "fullName=Test User" \
  -F "age=25" \
  -F "cityLastSeen=Test City" \
  -F "dateLastSeen=2024-01-15" \
  -F "contactPhone=1234567890" \
  -F "images=@/path/to/test-image.jpg"
```

### Test 3: Check Firestore
1. Go to Firebase Console
2. Navigate to Firestore Database
3. You should see `upload` and `counselor` collections after making requests

## Still Having Issues?

1. **Check backend logs** - Look for error messages in the terminal where backend is running
2. **Check browser console** - Look for detailed error messages
3. **Verify all dependencies are installed**:
   ```bash
   # Backend
   cd backend
   pip list
   
   # Frontend
   cd frontend
   npm list
   ```
4. **Try restarting both servers** - Sometimes a simple restart fixes issues

## Quick Checklist

Before submitting, make sure:
- [ ] Backend is running on port 8000
- [ ] Frontend is running on port 3000
- [ ] Firebase is configured (serviceAccountKey.json or .env)
- [ ] No firewall blocking localhost connections
- [ ] All dependencies are installed
- [ ] Browser console shows no errors





