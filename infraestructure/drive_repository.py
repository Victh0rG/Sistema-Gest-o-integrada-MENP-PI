# Upload / Download Google Drive
import google_auth

#
# class DriveRepository():
#     def __init__(self):
#         self.google_auth = google_auth.GoogleAuth()

auth = google_auth.GoogleAuthManager()
if auth.login():
    drive = auth.get_drive_service()

    paths = ['sead']
    drive.files().create(
        body={
            'name' : paths[0],
            'mimeType' : 'application/vnd.google-apps.folder',
        }
    ).execute()





