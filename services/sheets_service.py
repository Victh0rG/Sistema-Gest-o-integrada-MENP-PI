
from infraestructure import google_auth
from infraestructure import Authenticate
from dotenv import load_dotenv
import os

load_dotenv()

class SheetsService:
    def __init__(self):
        self.auth = Authenticate().authenticate()
        self.sheets = self.auth["sheets"]
        self.sheets_file = None

    def create_sheet(self, title: str):
        """
        cria um google sheet

        Parâmetros
        ----------
        title : nome da planinha

        """
        sheet_body = {
            "properties": {
                "title": title
            },
            'sheets': [
                {
                    "properties": {
                        "title": title
                    }
                }
            ]
        }

        self.sheets_file = self.sheets.spreadsheets().create(
            body=sheet_body
        ).execute()

        print(self.sheets_file)
        return self.sheets_file


    def create_page_sheet(self, title: str):
        """
        Adiciona uma nova aba (página) à planilha existente.

        Parâmetros
        ----------
        title : nome da nova aba

        """
        spreadsheet_id = os.getenv("SHEET_ID")

        request = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title
                        }
                    }
                }
            ]
        }

        page_sheet = self.sheets.spreadsheets().batchUpdate(
            spreadsheetId = spreadsheet_id,
            body = request
        ).execute()
        return page_sheet

