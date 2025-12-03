# Quick Fix: Firebase Credentials Error

## The Error You're Seeing

```
DefaultCredentialsError: Your default credentials were not found
```

This means the backend can't find your Firebase credentials.

## Quick Solution (Choose ONE method)

### Method 1: Use JSON File (Easiest) ⭐

1. **Get your Firebase service account key:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Select your project
   - Click ⚙️ (gear icon) → **Project settings**
   - Go to **Service accounts** tab
   - Click **"Generate new private key"**
   - Download the JSON file

2. **Rename and place the file:**
   - Rename the downloaded file to: `serviceAccountKey.json`
   - Move it to: `backend/serviceAccountKey.json`
   
   Your file structure should look like:
   ```
   backend/
     ├── serviceAccountKey.json  ← Place it here
     ├── main.py
     └── ...
   ```

3. **Restart the backend:**
   ```bash
   python main.py
   ```

### Method 2: Use .env File

1. **Create a `.env` file** in the `backend` folder:
   - Copy `env_template.txt` and rename it to `.env`

2. **Get your Firebase service account key** (same as Method 1, step 1)

3. **Open the downloaded JSON file** and copy its **entire contents**

4. **Paste it in `.env`** after `FIREBASE_SERVICE_ACCOUNT_KEY=`
   - Make sure it's all on ONE line
   - Wrap it in single quotes: `FIREBASE_SERVICE_ACCOUNT_KEY='{...}'`

5. **Install python-dotenv** (if not already installed):
   ```bash
   pip install python-dotenv
   ```

6. **Restart the backend:**
   ```bash
   python main.py
   ```

## Verify It's Working

After setting up credentials, you should see:
```
✅ Firebase credentials loaded from serviceAccountKey.json
✅ Firebase Admin SDK initialized successfully
✅ Firestore client connected
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Still Having Issues?

1. **Check the file is in the right place:**
   ```bash
   # Windows
   dir backend\serviceAccountKey.json
   
   # Linux/Mac
   ls backend/serviceAccountKey.json
   ```

2. **Check the JSON file is valid:**
   - Open `serviceAccountKey.json` in a text editor
   - Make sure it starts with `{` and ends with `}`
   - Make sure it's valid JSON (no syntax errors)

3. **For .env method, check the format:**
   - Should be: `FIREBASE_SERVICE_ACCOUNT_KEY='{...}'`
   - All on one line
   - Single quotes around the JSON

4. **See detailed guide:** `backend/FIREBASE_SETUP.md`





