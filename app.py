from flask import Flask, request, render_template
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os
app = Flask(__name__)
credentials_dict = {
  "type": "service_account",
  "project_id": "automate-438804",
  "private_key_id": "0a185fe0ccd8ef589cd020aa3740bef3f8ee4b2a",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC1eHk2tX2PLWdi\nWdhcxUAGnRvWDIUlZkzGa3DnA4OSNjI5SqoUgGhFoGzyuWvQfNvDWG3OadHr2fsK\ng+Y9xzZcj6QpX7MZXHsrrzwOKRy9UfKevgYnVFshbj0/vk3OTzPrJCDTj/2YFOC4\nrz/SC97h6AjmUPZuaWAgZJZyr+ZBhGz/96SHAKikcEpsMU9aVWYWU5sxwqZxAGK1\nxbat649y3lLAtYMv9q8+ZSDHKo4f0jxUdeb+eANQZ3r+jQKj+8l1MtNic8VCDJNc\nBeYZLgzHMcvz2xI6y7jVx2KEHpsHx5fqamflGhivrv70S+D7l/xjQc/gPHBA+P4h\nWuRDWCApAgMBAAECggEAD+V4IcibcXi52RHTfAnr2kB2NSWG3tAzqsBz5Qqn4n2U\nn/PoSvA2Ih5D2O3Q8dQUKKwk/0tCACnpvaGxACmkm45aJCUt0kuJfxnENh3YFoX4\njbsJ3TVcn8SxQRWVqXxC6SbSqNGw1lsC1e7FFYxkZ2/c4rcGJUUeDmxdSPnbXtL5\nf5NxdRRJzMmhRiJ3clf4jEoV09S+BD/XsDVVy0T4EHHolKtoD1XSuhNLzf0AgFUE\nFtspZYHJ0M55kiOS6oucY1tOQtt/T7niAeIQNdaR/EL+k50N+zr2pE8F5bgK8cXH\nxurpr/UGFkPmcrf6SxO2bhIaCo6v++EvUB6k9Az8kQKBgQD8qQGDpkLUJKijpG9h\n0zO8sXbvoD24mTcbrsJcSBOHZiX+kgJwCm9f5C9wcnDTnpJARHCbzWu4qw+cnnlF\nfTvvrIgz9liUbJv3whXBTLXmgfJ/klyKnIAQEbMzJZrDflbeEsbKFdzpNWeseL1O\nTKKnpadhaCc9Q8U4al+FfrMO2QKBgQC33pB0vocy0IGwTNa1u//kreSbpxOde2WX\n+5oZFPVDgDuJGsuLvHq5/osRBc+bcUSxUISjfnPN5OQtyhsmYPgj/LsSdrO+zmtG\nMHIdlxuCx5Hbgb7Zp+WDwM+IALNb70eTdMIHiHM8NQKieIFyDlX6uT4v2qZhH2LR\n6fmwa2Jp0QKBgQCrNvACwZlJ32m0MwsTlKbbuLrrWYBZ5uH0TXICTQmG2I7ouxMR\nz9B3f88x+StCDJP5HyfcPNFBvBIBRVbS4zHJkfZemBKgyhTLSWeqrQwbH3YwQwOZ\nHsKdoRD5mQMOdT/yj3DMoxInqvwNYWiPddlHmDccCBOHLbSpLVR7x0cZyQKBgHCz\n+KHGo4JvMf9JqhYtTVXzjPwntitCluxI6ZTUNt4QPO32Qau+dQ+Kyd0+TZn/HNb+\n/r5kZUFgOskiZ+/nYlJUuKpBnj2nszOLwHcIx3ErOOlupvgtJM7UoaDApTAGBD6L\nQ99wMQpHh/zklpu908/iOg8FHBTOMzluDIGp4OHxAoGBALGSlnFqO7VJSEYu52F2\naSP+z4iMPtzB5CZlXR/PtUu7TVCQ3T1vxsh7KSiRghwbzHbsq6ObG/zmnYdG0YlR\nufiGEGUwoin2wh2UIyvLEmuJnDT9UPr+CerzEjCdj8LLnV5xrNT0gqTzlHH5MPkK\nRE78K2WjoD1LiTe4uc+cyvYU\n-----END PRIVATE KEY-----\n",
  "client_email": "automate-service-account@automate-438804.iam.gserviceaccount.com",
  "client_id": "117172681632056896314",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/automate-service-account%40automate-438804.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
SCOPES = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
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
