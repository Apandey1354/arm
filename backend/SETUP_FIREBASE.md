# 🔥 Firebase Setup - Step by Step

## You need to set up Firebase credentials. Follow these steps:

### Step 1: Get Your Firebase Service Account Key

1. **Go to Firebase Console:**
   - Visit: https://console.firebase.google.com/
   - Sign in with your Google account

2. **Select or Create a Project:**
   - If you don't have a project, click "Add project" and create one
   - If you have a project, select it

3. **Get the Service Account Key:**
   - Click the **⚙️ gear icon** next to "Project Overview"
   - Select **"Project settings"**
   - Go to the **"Service accounts"** tab
   - Make sure **"Python"** is selected in the dropdown
   - Click **"Generate new private key"**
   - A dialog will appear - click **"Generate key"**
   - A JSON file will download (e.g., `your-project-firebase-adminsdk-xxxxx.json`)

### Step 2: Choose Your Setup Method

You have TWO options. Choose the one that's easier for you:

---

## ✅ OPTION A: Use JSON File (EASIEST - Recommended)

1. **Rename the downloaded file:**
   - Find the downloaded JSON file (usually in your Downloads folder)
   - Rename it to: `serviceAccountKey.json`

2. **Move it to the backend folder:**
   - Copy the file
   - Paste it into: `backend/serviceAccountKey.json`
   
   Your file structure should be:
   ```
   backend/
     ├── serviceAccountKey.json  ← Your file here
     ├── main.py
     └── ...
   ```

3. **Done!** Restart your backend:
   ```bash
   python main.py
   ```

---

## ✅ OPTION B: Use .env File

1. **Create a `.env` file:**
   - In the `backend` folder, create a new file named `.env`
   - (You can copy `env_template.txt` and rename it to `.env`)

2. **Open the downloaded JSON file:**
   - Open the JSON file you downloaded from Firebase
   - Select ALL the content (Ctrl+A / Cmd+A)
   - Copy it (Ctrl+C / Cmd+C)

3. **Paste it in `.env`:**
   - Open `backend/.env`
   - Add this line:
     ```env
     FIREBASE_SERVICE_ACCOUNT_KEY='{paste your JSON here}'
     ```
   - **IMPORTANT:** 
     - Keep it all on ONE line (no line breaks)
     - Wrap it in single quotes: `'...'`
     - Make sure you paste the ENTIRE JSON (starts with `{` and ends with `}`)

4. **Example of what it should look like:**
   ```env
   FIREBASE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"your-project","private_key_id":"abc123","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com",...}'
   ```

5. **Install python-dotenv** (if not already installed):
   ```bash
   pip install python-dotenv
   ```

6. **Done!** Restart your backend:
   ```bash
   python main.py
   ```

---

## ✅ Verify It's Working

After setting up credentials and restarting, you should see:

```
✅ Firebase credentials loaded from serviceAccountKey.json
✅ Firebase Admin SDK initialized successfully
✅ Firestore client connected
INFO:     Uvicorn running on http://0.0.0.0:8000
```

If you see errors, check the troubleshooting section below.

---

## 🔧 Troubleshooting

### "File not found" error
- Make sure `serviceAccountKey.json` is in the `backend` folder (same folder as `main.py`)
- Check the filename is exactly `serviceAccountKey.json` (case-sensitive)

### "Invalid JSON" error (for .env method)
- Make sure the JSON is all on ONE line
- Check you copied the ENTIRE JSON (from `{` to `}`)
- Make sure it's wrapped in single quotes: `'...'`

### "Module 'dotenv' not found"
- Run: `pip install python-dotenv`

### Still having issues?
- Try Option A (JSON file) - it's simpler
- Check `backend/FIREBASE_SETUP.md` for more detailed instructions
- Make sure Firestore is enabled in your Firebase project

---

## 📝 Quick Checklist

- [ ] Firebase project created
- [ ] Service account key downloaded
- [ ] Credentials file placed in backend folder (JSON or .env)
- [ ] Backend restarted
- [ ] See success messages (✅) when starting backend

---

**Need help?** Check `backend/FIREBASE_SETUP.md` for more details.





