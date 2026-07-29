import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import config

def get_gmail_service():
    """Authenticates and returns the Gmail service."""
    creds = None
    # Load token if it exists (stores user session)
    if os.path.exists(config.TOKEN_FILE):
        with open(config.TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
            
    # If no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.CREDENTIALS_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(config.TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def fetch_unread_emails(service):
    """Fetches list of unread messages from Inbox."""
    # Query: is:unread in:inbox
    results = service.users().messages().list(userId='me', q='is:unread in:inbox').execute()
    return results.get('messages', [])

def mark_email_as_read(service, msg_id):
    """Removes the UNREAD label from a message."""
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()