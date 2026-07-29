import sys
import os

# --- FIX START: Add parent directory to path ---
# This allows python to find 'config.py' which is outside the 'src' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# --- FIX END ---

import json
import config
from gmail_service import get_gmail_service, fetch_unread_emails, mark_email_as_read
from sheets_service import get_sheets_service, append_to_sheet
from email_parser import parse_email

# --- State Management ---
def load_state():
    """Loads the set of processed email IDs from a file."""
    if os.path.exists(config.STATE_FILE):
        with open(config.STATE_FILE, 'r') as f:
            try:
                return set(json.load(f))
            except json.JSONDecodeError:
                return set()
    return set()

def save_state(processed_ids):
    """Saves the processed email IDs to a file."""
    with open(config.STATE_FILE, 'w') as f:
        json.dump(list(processed_ids), f)

def main():
    print("--- Starting Gmail-to-Sheets Automation ---")
    
    # 1. Authenticate Services
    print("Authenticating...")
    gmail = get_gmail_service()
    sheets = get_sheets_service()
    
    # 2. Load State (Duplicate Prevention)
    processed_ids = load_state()
    print(f"Loaded {len(processed_ids)} previously processed IDs.")
    
    # 3. Fetch Unread Emails
    messages = fetch_unread_emails(gmail)
    print(f"Found {len(messages)} unread emails in Inbox.")

    if not messages:
        print("No new emails found. Exiting.")
        return

    new_processed_count = 0

    for msg in messages:
        msg_id = msg['id']

        # Strict duplicate check (State + Unread Status)
        if msg_id in processed_ids:
            print(f"Skipping duplicate (already in state): {msg_id}")
            continue

        try:
            # 4. Parse Email
            data = parse_email(gmail, msg_id)
            print(f"Processing: {data['subject']} (From: {data['from']})")

            # 5. Append to Sheets
            row = [data['from'], data['subject'], data['date'], data['content']]
            append_to_sheet(sheets, row)
            print(" -> Added to Sheet")

            # 6. Mark as Read
            mark_email_as_read(gmail, msg_id)
            print(" -> Marked as Read")

            # 7. Update State immediately in memory
            processed_ids.add(msg_id)
            new_processed_count += 1

        except Exception as e:
            print(f"Error processing message {msg_id}: {e}")

    # 8. Save state to file
    save_state(processed_ids)
    print("-------------------------------------------")
    print(f"Success! Processed {new_processed_count} new emails.")
    print("-------------------------------------------")

if __name__ == '__main__':
    main()