from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import json

SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_ID = '1TE90qtOXN1qqaPpNPyf81aTeJvVd9Zm3'  
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def list_files_in_folder(folder_id, prefix):
    links = []
    files_data = [] 
    query = f"'{folder_id}' in parents and trashed = false"
    page_token = None

    while True:
        results = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)",
            pageToken=page_token
        ).execute()

        files = results.get('files', [])
        for file in files:
            if file['name'].startswith(prefix):  
                download_link = f"https://drive.google.com/uc?id={file['id']}"
                files_data.append((file['name'], download_link))

        page_token = results.get('nextPageToken', None)
        if not page_token:
            break

    files_data_sorted = sorted(files_data, key=lambda x: x[0])
    links = [link for _, link in files_data_sorted]
    return links


