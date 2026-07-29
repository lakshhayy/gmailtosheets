# Gmail to Sheets Automation

## 1. High-Level Architecture
This diagram outlines the data flow from the Gmail API to the final Google Sheet.

```mermaid
graph TD
    User[User] -->|Authenticates (OAuth 2.0)| Script[Python Script]
    Script -->|1. Fetch Unread Emails| Gmail[Gmail API]
    Gmail -->|Return Email Data| Script
    Script -->|2. Check for Duplicates| State{processed_state.json}
    State -- ID Found --> Skip[Skip Email]
    State -- ID Not Found --> Process[3. Parse Content]
    Process -->|4. Append Row| Sheets[Google Sheets API]
    Process -->|5. Mark as Read| Gmail
    Process -->|6. Save ID| State

```

---

## 2. Setup Instructions

**Prerequisites:** Python 3, Google Cloud Project with Gmail & Sheets APIs enabled.

1. **Clone the Repository:**

2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Configure Credentials:**
* Place your downloaded `credentials.json` file inside the `credentials/` folder.
* Open `config.py` and add your **Spreadsheet ID** to the `SPREADSHEET_ID` variable.


4. **Run the Application:**
```bash
python3 src/main.py

```



---

## 3. Design Explanation

### OAuth Flow Used

I implemented **OAuth 2.0 for Desktop Applications** (Authorization Code Flow).

* **Reasoning:** Since this is a local automation script running on a personal machine, acting on behalf of a user (me) rather than a server, the Desktop flow is the standard security practice. It avoids storing sensitive passwords and uses a renewable `token.json` for subsequent runs.

### Duplicate Prevention Logic

Duplicate prevention is handled using a **"Check-then-Act"** strategy:

1. **Pre-Check:** The script loads a set of previously processed Message IDs from `processed_state.json`.
2. **Filter:** Before processing an email, it checks `if msg_id in processed_ids`. If true, the email is skipped immediately, even if it is still marked "Unread" in Gmail.
3. **Post-Action:** Only after successfully writing to the Sheet is the ID added to the state list.

### State Persistence Method

State is persisted in a local file named `processed_state.json`.

* **Format:** A simple JSON list of strings (Message IDs).
* **Why:** This provides a lightweight, serverless database. It ensures that if the script crashes halfway through or if an email is manually marked "Unread" again, the system remembers it has already been logged.

---

## 4. Challenges Faced & Solutions

**Challenge: Handling Messy HTML Email Bodies**
The Gmail API returns email content in a complex JSON structure (MIME parts). Some emails are plain text, while others are HTML with nested `div` and `span` tags. Simply extracting the payload resulted in unreadable, tag-heavy text in the spreadsheet.

**Solution:**
I implemented a robust parsing function in `email_parser.py` using the **BeautifulSoup** library.

1. The script first looks for a `text/plain` MIME part.
2. If not found, it takes the `text/html` part and uses `BeautifulSoup(html, "html.parser").get_text()` to strip all tags.
3. This ensures the spreadsheet contains clean, human-readable text regardless of the email format.

---

## 5. Limitations

1. **Local State Dependency:** If the `processed_state.json` file is deleted locally, the duplicate prevention history is lost, and old emails might be re-processed if they are still unread.
2. **Single User Only:** The script is designed for a single user. It does not support multi-tenancy (multiple users logging in simultaneously).
3. **Attachment Handling:** The current implementation processes text content only. Attachments (PDFs, images) are ignored.

---

**Author:** Lakshay | DTU

