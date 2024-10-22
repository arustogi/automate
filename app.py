from flask import Flask, request, render_template
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import base64
import json
import os
app = Flask(__name__)
SCOPES = ['https://www.googleapis.com/auth/drive.file']
encoded_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Decode the base64 string back to JSON format
key_json = base64.b64decode(encoded_key).decode('utf-8')

# Load the JSON key into credentials
credentials = service_account.Credentials.from_service_account_info(json.loads(key_json))
drive_service = build('drive', 'v3', credentials=credentials)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['pdf']
        if file:
            file.save(file.filename)
            media = MediaFileUpload(file.filename, mimetype='application/pdf')
            drive_service.files().create(
                media_body=media,
                body={'name': file.filename, 'parents': ['1kP7PS88Z7d71-9x80UmRaSaQsey1QY0P']}
            ).execute()
            os.remove(file.filename)
            return render_template('index.html', message="File uploaded successfully!")
    return render_template('index.html')
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
