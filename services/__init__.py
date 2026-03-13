from infraestructure import google_auth
import drive_service
import sheets_service

auth = google_auth.GoogleAuthManager()
if auth.login():
    sheets = auth.get_sheets_service()
    drive = auth.get_drive_service()
# _Drive = drive_service.DriveService()
# root_id  = _Drive.create_folder("MENP-PI")
# year_id  = _Drive.create_folder("2025",        parent_id=root_id)
# month_id = _Drive.create_folder("06 - Junho",  parent_id=year_id)
# meet_id  = _Drive.create_folder("Reuniao Ordinaria 03-06", parent_id=month_id)


sheets = sheets_service.SheetsService()
# sheets.create_sheet()
sheets.create_page_sheet()