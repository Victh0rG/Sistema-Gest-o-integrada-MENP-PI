
from infraestructure import google_auth
from infraestructure import Authenticate

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetsService:
    def __init__(self):
        self.auth = Authenticate().authenticate()
        self.sheets = self.auth["sheets"]
        self.sheets_file = None

    def create_sheet(self):
        """cria um google sheet"""
        sheet_body = {
            "properties": {
                "title": "MENP"
            },
            'sheets': [
                {
                    "properties": {
                        "title": "MENP"
                    }
                }
            ]
        }

        self.sheets_file = self.sheets.spreadsheets().create(
            body=sheet_body
        ).execute()

        print(self.sheets_file)
        return self.sheets_file


    def create_page_sheet(self):
        """cria uma nova página na planinha """
        spreadsheet_id = "1t0O-596AHu7uNoSvWSZUmDf6zdnEztSmQeiOzkPlH5I"

        request = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": "Página 2"
                        }
                    }
                }
            ]
        }
        page = self.sheets.spreadsheets().batchUpdate(
            spreadsheetId = spreadsheet_id,
            body = request
        )
        upade_page = print(spreadsheet_id)
        return page


