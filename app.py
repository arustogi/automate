from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import base64
import json
import os
app = Flask(__name__)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

encoded_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
missing_padding = len(encoded_key) % 4
if missing_padding:
    encoded_key += '=' * (4 - missing_padding)
key_json = base64.b64decode(encoded_key).decode('utf-8')
credentials = service_account.Credentials.from_service_account_info(json.loads(key_json))
drive_service = build('drive', 'v3', credentials=credentials)
@app.route('/')
def home():
    return render_template('index.html')

# Upload Route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join('/your/upload/folder', filename)
            file.save(filepath)
            return redirect(url_for('home'))  
    return render_template('upload.html')

# PowerPoint Presentation Route
@app.route('/presentation')
def presentation():
    return render_template('presentation.html')
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
