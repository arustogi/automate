from flask import Flask, request, render_template
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

app = Flask(__name__)

# Define your Google Drive API scope and credentials file.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'cred.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['pdf']
        if file:
            # Save the file temporarily
            file.save(file.filename)
            # Create a media file upload object
            media = MediaFileUpload(file.filename, mimetype='application/pdf')
            # Upload the file to Google Drive
            drive_service.files().create(
                media_body=media,
                body={'name': file.filename, 'parents': ['automate']}
            ).execute()
            return render_template('index.html', message="File uploaded successfully!")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
