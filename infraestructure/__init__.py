
from . import google_auth

class Authenticate:
    """ Instancia da classe GoogleAuthManager para ouath2"""

    _instance = None

    def __init__(self):
        self.auth = google_auth.GoogleAuthManager()
        self.services = None

    def authenticate(self):

        if not self.services:
            if self.auth.login():
                self.services = {
                    "sheets": self.auth.get_sheets_service(),
                    "drive": self.auth.get_drive_service(),
                    "user": self.auth.get_user_info()
                }

        return self.services
