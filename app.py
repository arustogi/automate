# from flask import Flask, request, render_template
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google.oauth2 import service_account
# import base64
# import json
# import os
# app = Flask(__name__)
# SCOPES = ['https://www.googleapis.com/auth/drive.file']

# encoded_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# missing_padding = len(encoded_key) % 4
# if missing_padding:
#     encoded_key += '=' * (4 - missing_padding)
# key_json = base64.b64decode(encoded_key).decode('utf-8')
# credentials = service_account.Credentials.from_service_account_info(json.loads(key_json))
# drive_service = build('drive', 'v3', credentials=credentials)

# @app.route('/')
# def home():
#     return render_template('index.html')

# # Upload Route
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'pdf' not in request.files:
#             return "No file part", 400
#         file = request.files['pdf']
#         if file.filename == '':
#             return "No selected file", 400
#         file = request.files['pdf']
#         if file:
#             file.save(file.filename)
#             media = MediaFileUpload(file.filename, mimetype='application/pdf')
#             drive_service.files().create(
#                 media_body=media,
#                 body={'name': file.filename, 'parents': ['1kP7PS88Z7d71-9x80UmRaSaQsey1QY0P']}
#             ).execute()
#             os.remove(file.filename)
#             return render_template('upload.html', message="File uploaded successfully!")
#     return render_template('upload.html')
# # PowerPoint Presentation Route
# @app.route('/presentation')
# def presentation():
#     return render_template('presentation.html')


# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)





from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__)

# Define directories for uploads and outputs
UPLOAD_FOLDER = '/Users/revapoddar/Desktop/jerry_pipeline/uploads'
OUTPUT_FOLDER = '/Users/revapoddar/Desktop/jerry_pipeline/pdf_extract_table_and_figure/output_new'

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def upload_page():
    return render_template('upload.html')  # Create an HTML template with a form to upload PDF

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return redirect(request.url)
    file = request.files['pdf']
    
    # Check if the file is a PDF
    if file and file.filename.endswith('.pdf'):
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)  # Save the PDF
        
        # Run the main.sh script with the uploaded PDF file
        result = subprocess.run(['/Users/revapoddar/Desktop/jerry_pipeline/pdf_extract_table_and_figure/main.sh', pdf_path], capture_output=True, text=True)

        if result.returncode != 0:
            return f"Error during processing: {result.stderr}"
        
        # Redirect to a route to display the output or list of processed images
        return redirect(url_for('display_output'))
    else:
        return "Please upload a PDF file."

@app.route('/output')
def display_output():
    # List images in the output folder to display to the user
    images = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith(('.png', '.jpg'))]
    return render_template('output.html', images=images, output_folder=OUTPUT_FOLDER)

@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
