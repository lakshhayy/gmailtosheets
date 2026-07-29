import base64
from bs4 import BeautifulSoup

def clean_body(data):
    """Decodes base64 url-safe string."""
    # Urlsafe base64 can have '-' and '_' instead of '+' and '/'
    clean_data = data.replace("-", "+").replace("_", "/")
    return base64.urlsafe_b64decode(clean_data).decode('utf-8')

def parse_email(service, msg_id):
    """Fetches full email details and extracts required fields."""
    msg = service.users().messages().get(userId='me', id=msg_id).execute()
    payload = msg['payload']
    headers = payload.get('headers')

    email_data = {
        'from': '',
        'subject': '',
        'date': '',
        'content': ''
    }

    # 1. Extract Headers
    for header in headers:
        name = header['name'].lower()
        if name == 'from':
            email_data['from'] = header['value']
        elif name == 'subject':
            email_data['subject'] = header['value']
        elif name == 'date':
            email_data['date'] = header['value']

    # 2. Extract Body (Plain text preferred)
    parts = payload.get('parts')
    body_content = ""
    
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body_content = part['body']['data']
                break  # Prefer plain text
            elif part['mimeType'] == 'text/html':
                # Fallback to HTML if plain text isn't found immediately
                body_content = part['body']['data']
    elif 'body' in payload and 'data' in payload['body']:
        # If the email has no parts (simple email)
        body_content = payload['body']['data']

    if body_content:
        try:
            decoded_html = clean_body(body_content)
            # Convert HTML to text to meet the "Content" requirement nicely
            soup = BeautifulSoup(decoded_html, "html.parser")
            email_data['content'] = soup.get_text().strip()
        except Exception as e:
            print(f"Error parsing body for {msg_id}: {e}")
            email_data['content'] = "(Error parsing content)"
    
    return email_data