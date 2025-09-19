from .math.calculator import calculator
from .entertainment.jokes import tell_joke

# Gmail tools - optional import (graceful fallback if dependencies not installed)
try:
    from .email.gmail import search_gmail, count_unread_gmail, read_gmail_message, get_recent_gmail
    gmail_tools = [search_gmail, count_unread_gmail, read_gmail_message, get_recent_gmail]
    __all__ = ['calculator', 'tell_joke', 'search_gmail', 'count_unread_gmail', 'read_gmail_message', 'get_recent_gmail']
except ImportError:
    gmail_tools = []
    __all__ = ['calculator', 'tell_joke']

# All available tools
all_tools = [calculator, tell_joke] + gmail_tools