# helper_list_folders.py
from cloud.google_drive_client import GoogleDriveClient

drive = GoogleDriveClient()
results = drive.service.files().list(
    q="mimeType='application/vnd.google-apps.folder'",
    fields="files(id, name)"
).execute()

folders = results.get('files', [])
print("\n📁 Your Folders:\n")
for f in folders:
    print(f"Name: {f['name']} | ID: {f['id']}")
