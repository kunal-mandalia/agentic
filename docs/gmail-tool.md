# Gmail Tools Setup Guide

This guide explains how to set up Gmail tools for smolagents to read and search your Gmail account with structured data responses.

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

### 2. OAuth 2.0 Setup (Recommended for Personal Gmail)

1. Go to "APIs & Services" > "OAuth consent screen"
2. Configure consent screen:
   - **User Type**: Choose "External" (unless you have Google Workspace)
   - Fill in required fields (App name, User support email, Developer contact)
   - **Scopes**: Add `https://www.googleapis.com/auth/gmail.readonly`
   - **Test users**: Add your Gmail address to test users list
3. Go to "APIs & Services" > "Credentials"
4. Click "Create Credentials" > "OAuth 2.0 Client ID"
5. Choose "Desktop application"
6. Download the credentials file
7. Save as your desired location (default: `../../../agentic/secrets/gcloud_desktop_credentials.json`)

## Environment Setup

Update the credentials path in your Gmail tools if needed:
```python
# In tools/email/gmail.py, update the path to your credentials
credentials_path = '../../../agentic/secrets/gcloud_desktop_credentials.json'
```

## Installation

Gmail dependencies are already included if you followed the main setup:

```bash
uv add google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

## Gmail Tools - Structured Data Implementation

### Available Tools with Structured Responses

#### 1. `search_gmail(query, max_results=10)`

**Returns structured dictionary:**
```python
{
  "query": "from:example@gmail.com",
  "total_found": 5,
  "messages": [
    {
      "id": "msg_123456",
      "subject": "Meeting Tomorrow",
      "sender": "boss@company.com",
      "date": "Mon, 18 Sep 2025 10:30:00 -0700",
      "snippet": "Don't forget our meeting at 2pm...",
      "body": "",
      "is_unread": true
    }
    // ... more messages
  ]
}
```

**Example queries:**
- `search_gmail("is:unread")` - Find unread emails
- `search_gmail("from:john@example.com")` - Emails from specific sender
- `search_gmail("subject:invoice")` - Emails with "invoice" in subject
- `search_gmail("newer_than:7d")` - Emails from last 7 days

#### 2. `count_unread_gmail()`

**Returns structured dictionary:**
```python
{
  "unread_count": 100,
  "message": "You have 100 unread messages.",
  "has_unread": true
}
```

#### 3. `read_gmail_message(message_id)`

**Returns structured dictionary:**
```python
{
  "id": "msg_123456",
  "subject": "Meeting Tomorrow",
  "sender": "boss@company.com",
  "date": "Mon, 18 Sep 2025 10:30:00 -0700",
  "snippet": "Don't forget our meeting...",
  "body": "Full email body content here...",
  "is_unread": true
}
```

#### 4. `get_recent_gmail(count=5)`

**Returns structured dictionary:**
```python
{
  "query": "recent",
  "total_found": 5,
  "messages": [
    // Array of EmailMessage objects (same structure as search_gmail)
  ]
}
```

### Benefits of Structured Data

✅ **Type-safe access** - Agent can access specific attributes like `.unread_count`, `.has_unread`
✅ **No string parsing** - Direct access to data fields
✅ **Better error handling** - Structured error responses
✅ **Composable queries** - Agent can build complex logic using individual fields
✅ **Self-correcting** - Agent learns to handle structured data automatically

### Usage Examples in Agent

```python
# The agent can now work with structured data intelligently:

# Simple count with boolean logic
result = agent.run("Do I have unread emails? Give me exact count and true/false.")
# Agent accesses: result['unread_count'] and result['has_unread']

# Complex search with attribute access
result = agent.run("Find emails from last week and tell me who sent the most recent one")
# Agent accesses: messages[0]['sender'], messages[0]['date']

# Structured filtering
result = agent.run("Search for unread emails and show me only the subjects")
# Agent accesses: [msg['subject'] for msg in messages if msg['is_unread']]
```

## First-Time Authentication

1. Run your smolagents application
2. When prompted, a browser window will open for Google OAuth
3. Sign in with your Google account
4. Grant permissions to access Gmail (read-only)
5. Authentication token will be saved automatically for future use

## Security Considerations

1. **Credentials are in `.gitignore`** - Never commit credential files
2. **Read-only access** - Tools only request Gmail read permissions
3. **Token caching** - Authentication token cached locally in `token.pickle`
4. **Secure paths** - Credentials stored outside project directory

## Troubleshooting

### "Client secrets must be for a web or installed app"
- You're using service account credentials instead of OAuth 2.0
- Download OAuth 2.0 credentials for "Desktop application"

### "App is in testing mode"
- Add your email to "Test users" in OAuth consent screen
- Or publish your app (not recommended for personal use)

### "Authentication failed"
- Delete `token.pickle` and re-authenticate
- Check that Gmail API is enabled in Google Cloud Console

### "Credentials not found"
- Verify the credentials file path in `tools/email/gmail.py`
- Ensure file exists at specified location

## Example Agent Interactions

```bash
# Count unread emails
agent.run("How many unread emails do I have?")
# Returns: "You have 100 unread messages."

# Search with structured response
agent.run("Find emails from john@example.com from last week")
# Agent gets structured data and can access sender, date, subject individually

# Complex query with data manipulation
agent.run("Search unread emails and tell me the top 3 senders")
# Agent processes structured message list and counts by sender
```

The Gmail tools now provide rich, structured data that enables more intelligent agent interactions and reliable email processing.