import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
load_dotenv()

def get_sheet():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = os.path.join(BASE_DIR, "credentials.json")

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        creds_path, 
        scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("College Event Registrations").sheet1
    return sheet

def save_to_sheet(row):
    sheet = get_sheet()
    sheet.append_row(row)


