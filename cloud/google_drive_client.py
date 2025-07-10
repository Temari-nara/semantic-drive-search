# cloud/google_drive_client.py

import os
import io
from typing import List
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import List
from googleapiclient.http import MediaIoBaseDownload

class GoogleDriveClient:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None
        self.service = self.authenticate()

    def authenticate(self):
        """Authenticate using OAuth2 and return the Drive API service."""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
            self.creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token_file:
                token_file.write(self.creds.to_json())

        return build('drive', 'v3', credentials=self.creds)

    def list_supported_files(self, mime_types=None) -> List[dict]:
        """List supported files from a folder using folder_id from .env"""
        if mime_types is None:
            mime_types = [
                "application/pdf",
                "text/plain",
                "text/csv",
                "image/png"
            ]

        # Replace with your actual folder ID
        folder_id = os.getenv("DRIVE_FOLDER_ID")
        if not folder_id:
            raise ValueError(" DRIVE_FOLDER_ID is not set in the .env file.")

        query = f"('{folder_id}' in parents) and ({' or '.join([f'mimeType=\'{mime}\'' for mime in mime_types])})"


        results = self.service.files().list(
            q=query,
            pageSize=50,
            fields="files(id, name, mimeType, webViewLink)"
        ).execute()

        return results.get('files', [])


    def authenticate(self):
        """Authenticate using OAuth2 and return the Drive API service."""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
            self.creds = flow.run_local_server(port=8080)  # 🔥 FIXED PORT
            with open(self.token_path, 'w') as token_file:
                token_file.write(self.creds.to_json())

        return build('drive', 'v3', credentials=self.creds)


    def download_file(self, file_id: str, file_name: str, download_path='downloads') -> str:
        """Download a file by ID and save locally."""
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        request = self.service.files().get_media(fileId=file_id)
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

        return file_path
