import os
import pickle
from googleapiclient.discovery import build
import config

def get_sheets_service():
    """Authenticates and returns the Sheets service using the same token."""
    # We reuse the token file created by the Gmail login to avoid double login
    creds = None
    if os.path.exists(config.TOKEN_FILE):
        with open(config.TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
            
    return build('sheets', 'v4', credentials=creds)

def append_to_sheet(service, values):
    """Appends a row of data to the configured Google Sheet."""
    body = {
        'values': [values]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=config.SPREADSHEET_ID,
        range=config.RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()
    return result