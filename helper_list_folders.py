# # helper_list_folders.py
# from cloud.google_drive_client import GoogleDriveClient

# drive = GoogleDriveClient()
# results = drive.service.files().list(
#     q="mimeType='application/vnd.google-apps.folder'",
#     fields="files(id, name)"
# ).execute()

# folders = results.get('files', [])
# print("\n📁 Your Folders:\n")
# for f in folders:
#     print(f"Name: {f['name']} | ID: {f['id']}")

# helper_list_folders.py

from cloud.google_drive_client import GoogleDriveClient

def get_all_drive_folders():
    drive = GoogleDriveClient()
    results = drive.service.files().list(
        q="mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)",
        pageSize=100
    ).execute()

    return results.get('files', [])

# Optional: allow CLI run
if __name__ == "__main__":
    folders = get_all_drive_folders()
    print("\n📁 Your Folders:\n")
    for f in folders:
        print(f"Name: {f['name']} | ID: {f['id']}")
