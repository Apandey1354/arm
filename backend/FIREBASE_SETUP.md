# Firebase Setup Guide

This guide will walk you through setting up Firebase for the FindMe backend.

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter a project name (e.g., "FindMe" or "MissingPersonPlatform")
4. Click **"Continue"**
5. (Optional) Enable Google Analytics - you can skip this for now
6. Click **"Create project"**
7. Wait for the project to be created, then click **"Continue"**

## Step 2: Enable Firestore Database

1. In your Firebase project dashboard, click on **"Firestore Database"** in the left sidebar
2. Click **"Create database"**
3. Choose **"Start in test mode"** (for development) or **"Start in production mode"** (for production)
   - **Test mode**: Allows read/write access for 30 days, then you'll need to set up security rules
   - **Production mode**: Requires security rules from the start
4. Select a **location** for your database (choose the closest to your users)
5. Click **"Enable"**
6. Wait for Firestore to be set up

### Setting Up Security Rules (Important!)

After enabling Firestore, you should set up security rules:

1. Go to **Firestore Database** → **Rules** tab
2. For development, you can use these rules (⚠️ **NOT for production**):
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read, write: if request.auth != null;
       }
     }
   }
   ```
3. For production, you'll want more restrictive rules. For now, since we're using Admin SDK, the rules can be:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /{document=**} {
         allow read, write: if false; // Only Admin SDK can access
       }
     }
   }
   ```
4. Click **"Publish"**

## Step 3: Get Service Account Key

1. In Firebase Console, click the **gear icon** (⚙️) next to "Project Overview"
2. Select **"Project settings"**
3. Go to the **"Service accounts"** tab
4. You'll see "Firebase Admin SDK"
5. Make sure **"Python"** is selected in the language dropdown
6. Click **"Generate new private key"**
7. A dialog will appear - click **"Generate key"**
8. A JSON file will be downloaded to your computer (e.g., `findme-firebase-adminsdk-xxxxx.json`)

## Step 4: Add Service Account Key to Backend

1. **Rename the downloaded file** to `serviceAccountKey.json`
2. **Move the file** to your `backend` directory:
   ```
   backend/
     ├── serviceAccountKey.json  ← Place it here
     ├── main.py
     ├── image_processor.py
     └── ...
   ```

⚠️ **IMPORTANT SECURITY NOTE:**
- Never commit `serviceAccountKey.json` to Git (it's already in `.gitignore`)
- Keep this file secure - it gives full access to your Firebase project
- If you accidentally commit it, regenerate a new key immediately

## Step 5: Verify Firebase Setup

1. Make sure your `backend` directory structure looks like this:
   ```
   backend/
     ├── serviceAccountKey.json
     ├── main.py
     ├── image_processor.py
     ├── requirements.txt
     └── ...
   ```

2. Test the connection by running:
   ```bash
   cd backend
   python main.py
   ```

3. If everything is set up correctly, you should see:
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

4. Visit `http://localhost:8000` in your browser - you should see:
   ```json
   {"message":"FindMe Backend API is running"}
   ```

## Step 6: Test Firebase Connection

You can test if Firebase is working by checking the Firestore console:

1. After running the backend and making a test API call
2. Go to Firebase Console → Firestore Database
3. You should see two collections:
   - `upload` - for missing person reports
   - `counselor` - for counselor requests

## Alternative: Using Environment Variables

If you prefer not to store the JSON file, you can use environment variables:

1. Open the `serviceAccountKey.json` file
2. Copy its entire contents
3. Set it as an environment variable:
   
   **Windows (PowerShell):**
   ```powershell
   $env:FIREBASE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"...",...}'
   ```
   
   **Windows (CMD):**
   ```cmd
   set FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account","project_id":"...",...}
   ```
   
   **Linux/Mac:**
   ```bash
   export FIREBASE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"...",...}'
   ```

4. Remove or don't create the `serviceAccountKey.json` file
5. The backend will automatically use the environment variable

## Troubleshooting

### Error: "Failed to get project ID"
- Make sure `serviceAccountKey.json` is in the correct location
- Verify the JSON file is valid (not corrupted)
- Check that the file has the correct permissions

### Error: "Permission denied"
- Verify Firestore is enabled in your Firebase project
- Check that your service account has the correct permissions
- Make sure you're using the correct service account key

### Error: "Module not found: firebase_admin"
- Run: `pip install firebase-admin`

### Firestore not showing data
- Make sure you're looking at the correct Firebase project
- Check that the backend is actually running and receiving requests
- Verify the API calls are successful (check backend logs)

## Next Steps

Once Firebase is set up:

1. ✅ Your backend can now store data in Firestore
2. ✅ Test the upload endpoint with a sample image
3. ✅ Check Firestore console to see the data
4. ✅ Set up proper security rules for production
5. ✅ Consider using Firebase Storage for images instead of base64 (for better performance)

## Production Considerations

For production deployment:

1. **Use Firebase Storage** for images instead of storing base64 in Firestore
2. **Set up proper security rules** for Firestore
3. **Use environment variables** or secure secret management (not JSON files)
4. **Enable Firebase Authentication** if you need user authentication
5. **Set up Firebase Functions** for additional serverless functionality





