import google_auth

auth = google_auth.GoogleAuthManager()
if auth.login():
    sheets = auth.get_sheets_service()
    drive = auth.get_drive_service()
    user = auth.get_user_info()