from flask import Flask, request, render_template
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

app = Flask(__name__)

# Load Google Drive credentials from environment variables or use a JSON file
credentials_dict = {
    "type": os.environ['type'],
    "project_id": os.environ['project_id'],
    "private_key_id": os.environ['private_key_id'],
    "private_key": os.environ['private_key'].replace('\\n', '\n'),
    "client_email": os.environ['client_email'],
    "client_id": os.environ['client_id'],
    "auth_uri": os.environ['auth_uri'],
    "token_uri": os.environ['token_uri'],
    "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
    "client_x509_cert_url": os.environ['client_x509_cert_url']
}

credentials = service_account.Credentials.from_service_account_info(credentials_dict)

drive_service = build('drive', 'v3', credentials=credentials)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['pdf']
        if file:
            # Save the uploaded file temporarily
            file.save(file.filename)

            # Create a media file upload object for Google Drive
            media = MediaFileUpload(file.filename, mimetype='application/pdf')

            # Upload the file to Google Drive
            drive_service.files().create(
                media_body=media,
                body={'name': file.filename, 'parents': ['1kP7PS88Z7d71-9x80UmRaSaQsey1QY0P']}
            ).execute()

            # Remove the temporarily saved file after upload
            os.remove(file.filename)

            return render_template('index.html', message="File uploaded successfully!")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
