# Gmail Tools Setup Guide

This guide explains how to set up Gmail tools for smolagents to read and search your Gmail account.

## Prerequisites

1. Google Account with Gmail access
2. Google Cloud Project (free tier is sufficient)
3. Gmail API enabled for your project

## Gmail API Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### 2. Create Service Account (Recommended for Server)

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in service account details
4. Download the JSON key file
5. Save as `gmail-service-account.json` in your project root

### 3. OAuth Setup (For Personal Use)

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Choose "Desktop application"
4. Download `credentials.json`
5. Save in your project root

## Environment Setup

Add to your `.env` file:

```bash
# Gmail API Configuration
GMAIL_CREDENTIALS_PATH=./credentials.json
GMAIL_SERVICE_ACCOUNT_PATH=./gmail-service-account.json
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly

# For domain-wide delegation (G Suite/Workspace)
GMAIL_DELEGATED_USER=your-email@domain.com
```

## Installation

Add required dependencies:

```bash
uv add google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

## Gmail Tools Implementation

### Basic Gmail Search Tool

```python
# tools/email/gmail.py
from smolagents import tool
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Authenticate and return Gmail service object."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

@tool
def search_gmail(query: str, max_results: int = 10) -> str:
    """
    Search Gmail messages with a query.

    Args:
        query: Gmail search query (e.g., "from:example@gmail.com", "is:unread")
        max_results: Maximum number of results to return

    Returns:
        Formatted string with search results
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', q=query, maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            return f"No messages found for query: {query}"

        output = f"Found {len(messages)} messages for '{query}':\n\n"

        for msg in messages:
            msg_detail = service.users().messages().get(
                userId='me', id=msg['id']
            ).execute()

            headers = msg_detail['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'No Date')

            output += f"• {subject}\n"
            output += f"  From: {sender}\n"
            output += f"  Date: {date}\n"
            output += f"  ID: {msg['id']}\n\n"

        return output

    except Exception as e:
        return f"Error searching Gmail: {str(e)}"

@tool
def count_unread_gmail() -> str:
    """
    Count unread messages in Gmail.

    Returns:
        Number of unread messages
    """
    try:
        service = get_gmail_service()
        results = service.users().messages().list(
            userId='me', q='is:unread'
        ).execute()

        messages = results.get('messages', [])
        count = len(messages)

        return f"You have {count} unread messages."

    except Exception as e:
        return f"Error counting unread messages: {str(e)}"

@tool
def read_gmail_message(message_id: str) -> str:
    """
    Read a specific Gmail message by ID.

    Args:
        message_id: Gmail message ID

    Returns:
        Message content and metadata
    """
    try:
        service = get_gmail_service()
        message = service.users().messages().get(
            userId='me', id=message_id
        ).execute()

        headers = message['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'No Date')

        # Get message body
        body = ""
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
        else:
            if message['payload']['body'].get('data'):
                body = base64.urlsafe_b64decode(
                    message['payload']['body']['data']
                ).decode('utf-8')

        output = f"Subject: {subject}\n"
        output += f"From: {sender}\n"
        output += f"Date: {date}\n\n"
        output += f"Body:\n{body[:1000]}..."  # Truncate long messages

        return output

    except Exception as e:
        return f"Error reading message: {str(e)}"
```

## Security Considerations

1. **Never commit credentials** - Add `credentials.json`, `token.pickle`, and `gmail-service-account.json` to `.gitignore`
2. **Use least privilege** - Only request necessary Gmail scopes
3. **Rotate credentials** regularly for production use
4. **Consider service accounts** for server deployments

## Usage Examples

```python
# In your agent code
from tools.email.gmail import search_gmail, count_unread_gmail, read_gmail_message

# Add to your agent
agent = CodeAgent(tools=[
    calculator,
    tell_joke,
    search_gmail,
    count_unread_gmail,
    read_gmail_message
], model=model)

# Example queries:
# - "Search my emails from john@example.com"
# - "How many unread emails do I have?"
# - "Find emails with subject containing 'invoice'"
```

## Troubleshooting

- **Authentication errors**: Ensure credentials.json is valid and in project root
- **Scope errors**: Make sure you're using the correct Gmail API scopes
- **Rate limits**: Gmail API has quotas - implement backoff for production use
- **Large mailboxes**: Consider pagination for accounts with many emails

## Next Steps

1. Implement the Gmail tools in your `tools/email/` directory
2. Update `tools/__init__.py` to include email tools
3. Add Gmail tools to your agent configuration
4. Test with simple queries before complex searches