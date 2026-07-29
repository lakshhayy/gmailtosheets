# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration Settings ---

# 1. Google Sheet Setup
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
if not SPREADSHEET_ID:
    raise ValueError("SPREADSHEET_ID environment variable is not set. Please check your .env file.")
# The range to write to. "Sheet1!A:D" means it will look at columns A, B, C, and D.
RANGE_NAME = 'Sheet1!A:D'

# 2. File Paths
# These point to the credentials folder you created
CREDENTIALS_FILE = 'credentials/credentials.json'
TOKEN_FILE = 'credentials/token.json'
STATE_FILE = 'processed_state.json'

# 3. OAuth Scopes (Permissions)
# We need permission to Read/Modify Gmail and Read/Write Sheets
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]