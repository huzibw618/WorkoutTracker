import io
import os
import zipfile

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


class GdriveHandler():

    def __init__(self):
        self.scope = ["https://www.googleapis.com/auth/drive"]
        self.creds = self.getCredentials()
        self.service = build("drive", "v3", credentials=self.creds)

    def getCredentials(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scope)
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.scope)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as f:
                f.write(creds.to_json())
        return creds

    def getFolderId(self, folder_name):
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get("files", [])
        if not folders:
            raise FileNotFoundError(f"Folder '{folder_name}' not found in Drive")
        return folders[0]["id"]

    def getFileId(self, file_name, folder_id):
        query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])
        if not files:
            raise FileNotFoundError(f"File '{file_name}' not found in folder")
        return files[0]["id"]

    def getFile(self, file_id):
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
            return file.getvalue()
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def extractZip(self, file_bytes, extract_to="."):
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            z.extractall(extract_to)
            print(f"Extracted: {z.namelist()}")
            return z.namelist()

    def downloadFile(self, folder_name="Workouts", file_name="Workout", extract_to="./data"):
        folder_id = self.getFolderId(folder_name)
        file_id = self.getFileId(file_name, folder_id)
        file_bytes = self.getFile(file_id)
        return self.extractZip(file_bytes, extract_to)
