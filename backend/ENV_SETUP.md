# Setting Up Firebase with .env File

## Quick Steps

1. **Get your Firebase service account key:**
   - Go to Firebase Console → Project Settings → Service Accounts
   - Click "Generate new private key"
   - Download the JSON file

2. **Open the downloaded JSON file** and copy its **entire contents**

3. **Open `backend/.env`** file in a text editor

4. **Paste the JSON** after `FIREBASE_SERVICE_ACCOUNT_KEY=`
   
   **Important:** Make sure it's all on ONE line! Remove any line breaks.

5. **Save the file**

6. **Install dependencies** (if you haven't already):
   ```bash
   pip install -r requirements.txt
   ```

7. **Run the backend:**
   ```bash
   python main.py
   ```

## Example .env File

Your `.env` file should look like this:

```env
FIREBASE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"your-project-id","private_key_id":"abc123","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n","client_email":"firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project.iam.gserviceaccount.com"}'
```

## Important Notes

⚠️ **Keep it on ONE line** - The entire JSON must be on a single line in the .env file

⚠️ **Use single quotes** - Wrap the JSON in single quotes: `FIREBASE_SERVICE_ACCOUNT_KEY='{...}'`

⚠️ **Don't commit .env** - The .env file is already in .gitignore, so it won't be committed to Git

## Troubleshooting

### "Invalid JSON" error
- Make sure the JSON is on one line
- Check that you copied the entire JSON (including opening `{` and closing `}`)
- Make sure you're using single quotes around the JSON

### "Module 'dotenv' not found"
- Run: `pip install python-dotenv`

### Still not working?
- Try using the JSON file method instead (place `serviceAccountKey.json` in backend folder)
- The backend will automatically use whichever method is available

## Priority Order

The backend checks in this order:
1. **JSON file** (`serviceAccountKey.json`) - if it exists, uses this
2. **Environment variable** (from `.env` file) - if JSON file doesn't exist
3. **Default credentials** - for Google Cloud environments

So if you have both, the JSON file takes priority!





