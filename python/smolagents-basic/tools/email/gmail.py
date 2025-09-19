from smolagents import tool
import os
import pickle
import base64
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

@dataclass
class EmailMessage:
    """Structured email message data."""
    id: str
    subject: str
    sender: str
    date: str
    snippet: str = ""
    body: str = ""
    is_unread: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

@dataclass
class EmailSearchResult:
    """Structured search results."""
    query: str
    total_found: int
    messages: List[EmailMessage]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "query": self.query,
            "total_found": self.total_found,
            "messages": [msg.to_dict() for msg in self.messages]
        }

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Authenticate and return Gmail service object."""
    if not GMAIL_AVAILABLE:
        raise ImportError("Gmail dependencies not installed. Run: uv add google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2")

    creds = None
    token_path = 'token.pickle'
    credentials_path = '../../../agentic/secrets/gcloud_desktop_credentials.json'

    # Check if credentials.json exists
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Gmail credentials not found at {credentials_path}. "
            "Please follow the setup guide in GMAIL_SETUP.md"
        )

    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

@tool
def search_gmail(query: str, max_results: int = 10) -> Dict[str, Any]:
    """
    Search Gmail messages with a query.

    Args:
        query: Gmail search query (e.g., "from:example@gmail.com", "is:unread", "subject:invoice")
        max_results: Maximum number of results to return (1-50)

    Returns:
        Dictionary with search results including query, total found, and list of messages
        Each message has: id, subject, sender, date, snippet
    """
    try:
        if not GMAIL_AVAILABLE:
            return {"error": "Gmail tools not available. Please install dependencies: uv add google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2"}

        # Validate max_results
        max_results = max(1, min(50, max_results))

        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', q=query, maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            return EmailSearchResult(
                query=query,
                total_found=0,
                messages=[]
            ).to_dict()

        email_messages = []
        for msg in messages:
            try:
                msg_detail = service.users().messages().get(
                    userId='me', id=msg['id'], format='metadata',
                    metadataHeaders=['Subject', 'From', 'Date']
                ).execute()

                headers = msg_detail['payload'].get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'No Date')

                # Get snippet if available
                snippet = msg_detail.get('snippet', '')

                email_msg = EmailMessage(
                    id=msg['id'],
                    subject=subject,
                    sender=sender,
                    date=date,
                    snippet=snippet,
                    is_unread='UNREAD' in msg_detail.get('labelIds', [])
                )
                email_messages.append(email_msg)

            except Exception as e:
                # Add error message as an email entry
                email_msg = EmailMessage(
                    id=msg.get('id', 'unknown'),
                    subject=f"Error reading message: {str(e)}",
                    sender="Error",
                    date="Unknown"
                )
                email_messages.append(email_msg)

        return EmailSearchResult(
            query=query,
            total_found=len(email_messages),
            messages=email_messages
        ).to_dict()

    except FileNotFoundError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error searching Gmail: {str(e)}"}

@tool
def count_unread_gmail() -> Dict[str, Any]:
    """
    Count unread messages in Gmail.

    Returns:
        Dictionary with unread count and status message
    """
    try:
        if not GMAIL_AVAILABLE:
            return {"error": "Gmail tools not available. Please install dependencies first."}

        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', q='is:unread'
        ).execute()

        messages = results.get('messages', [])
        count = len(messages)

        return {
            "unread_count": count,
            "message": f"You have {count} unread message{'s' if count != 1 else ''}.",
            "has_unread": count > 0
        }

    except FileNotFoundError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Error counting unread messages: {str(e)}"}

@tool
def read_gmail_message(message_id: str) -> Dict[str, Any]:
    """
    Read a specific Gmail message by ID.

    Args:
        message_id: Gmail message ID (from search results)

    Returns:
        Dictionary with complete message details including subject, sender, date, body, and metadata
    """
    try:
        if not GMAIL_AVAILABLE:
            return "Gmail tools not available. Please install dependencies first."

        service = get_gmail_service()
        message = service.users().messages().get(
            userId='me', id=message_id, format='full'
        ).execute()

        headers = message['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'No Date')

        # Extract message body
        body = ""

        def extract_body(payload):
            """Recursively extract text body from message payload."""
            if payload.get('body', {}).get('data'):
                return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')

            if 'parts' in payload:
                for part in payload['parts']:
                    if part.get('mimeType') == 'text/plain':
                        if part.get('body', {}).get('data'):
                            return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                    elif part.get('mimeType') == 'multipart/alternative':
                        # Recursively check multipart content
                        nested_body = extract_body(part)
                        if nested_body:
                            return nested_body

            return ""

        body = extract_body(message['payload'])

        # Format output
        output = f"Subject: {subject}\n"
        output += f"From: {sender}\n"
        output += f"Date: {date}\n"
        output += f"Message ID: {message_id}\n\n"

        if body:
            # Truncate very long messages
            if len(body) > 2000:
                output += f"Body (truncated):\n{body[:2000]}...\n\n[Message truncated - {len(body)} total characters]"
            else:
                output += f"Body:\n{body}"
        else:
            output += "Body: [Unable to extract text content - may be HTML only or have attachments]"

        return output

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Error reading message {message_id}: {str(e)}"

@tool
def get_recent_gmail(count: int = 5) -> str:
    """
    Get recent Gmail messages.

    Args:
        count: Number of recent messages to retrieve (1-20)

    Returns:
        Formatted string with recent messages
    """
    try:
        if not GMAIL_AVAILABLE:
            return "Gmail tools not available. Please install dependencies first."

        # Validate count
        count = max(1, min(20, count))

        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', maxResults=count
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            return "No messages found in your Gmail."

        output = f"Your {len(messages)} most recent messages:\n\n"

        for i, msg in enumerate(messages, 1):
            try:
                msg_detail = service.users().messages().get(
                    userId='me', id=msg['id'], format='metadata',
                    metadataHeaders=['Subject', 'From', 'Date']
                ).execute()

                headers = msg_detail['payload'].get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'No Date')

                output += f"{i}. {subject}\n"
                output += f"   From: {sender}\n"
                output += f"   Date: {date}\n"
                output += f"   ID: {msg['id']}\n\n"
            except Exception as e:
                output += f"{i}. Error reading message: {str(e)}\n\n"

        return output.strip()

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Error getting recent messages: {str(e)}"