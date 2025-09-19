# Smolagents Basic Implementation

A minimal implementation of smolagents demonstrating local model orchestration with powerful tools.

## Architecture

This project demonstrates using a lightweight model (GPT-5-nano) as an orchestrator to control specialized tools, providing:
- **Cost-effective** - Cheap model handles routing/orchestration
- **Fast** - No heavy model loading for basic decisions
- **Scalable** - Add tools incrementally for specific use cases

## Project Structure

```
smolagents-basic/
├── tools/                    # Organized tool modules
│   ├── math/                # Mathematical operations
│   │   └── calculator.py    # Addition tool
│   └── entertainment/       # Fun/utility tools
│       └── jokes.py        # Joke generation
├── agents/                  # Agent configurations
│   └── basic_agent.py      # Main agent factory
├── main.py                 # Script version (loads model each run)
├── server.py               # Server version (loads model once)
└── README.md               # This file
```

## Model Requirements

**Key Learning**: Very small local models (< 3B parameters) struggle with smolagents' code generation format.

### Tested Models

L **TinyLlama-1.1B** - Too small, inconsistent code formatting
L **SmolLM-135M** - Missing chat template, too small for code generation
L **tinyagent-1.1b** - Generated text instead of proper code blocks
 **GPT-5-nano** - Reliable code generation, proper `final_answer()` usage

### Recommendation

For production use, stick with models 3B+ parameters or well-trained instruction-following models like GPT-4o-mini/GPT-5-nano for reliable smolagents orchestration.

## Setup

```bash
# Install dependencies
uv add smolagents flask litellm python-dotenv torch transformers accelerate

# For Gmail tools (optional)
uv add google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2

# Add OpenAI API key to .env
echo "OPENAI_API_KEY=your-key-here" > .env

# Run script version
uv run python main.py

# Run server version
uv run python server.py
# Test: curl -X POST http://localhost:5000/run -H 'Content-Type: application/json' -d '{"task": "tell me a joke"}'
```

### Gmail Setup

For Gmail tools, see [GMAIL_SETUP.md](./GMAIL_SETUP.md) for detailed OAuth 2.0 configuration and structured data examples.

**Quick setup:**
1. Create OAuth 2.0 credentials in Google Cloud Console
2. Add your email as test user
3. Download credentials and update path in `tools/email/gmail.py`
4. First run will open browser for authentication

## Tools

### Math Tools (`tools/math/`)
- `calculator(a, b)` - Add two numbers together

### Entertainment Tools (`tools/entertainment/`)
- `tell_joke()` - Returns a random joke

### Email Tools (`tools/email/`) ✅ **Implemented with Structured Data**
- `search_gmail(query, max_results)` - Search Gmail messages → Returns structured dict with messages array
- `read_gmail_message(message_id)` - Read specific email content → Returns structured email object
- `get_recent_gmail(count)` - Get recent emails → Returns structured messages list
- `count_unread_gmail()` - Count unread messages → Returns `{unread_count, message, has_unread}`

**Structured Data Benefits:**
- 🎯 **Type-safe access** - Agent can access `.unread_count`, `.has_unread`, `.subject` directly
- 🚫 **No string parsing** - Agent works with clean data structures instead of formatted text
- 🔧 **Self-correcting** - Agent learns to handle structured responses automatically
- 🏗️ **Composable** - Build complex queries using individual message attributes

### Adding New Tools

1. Create a new module in the appropriate `tools/` subdirectory
2. Use the `@tool` decorator on your functions
3. Add imports to the relevant `__init__.py` files
4. Update your agent configuration in `agents/basic_agent.py`

Example:
```python
# tools/math/advanced.py
from smolagents import tool

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
```

## Example Agent Interactions

**With structured Gmail data:**
```bash
# Agent gets structured response and accesses specific fields
agent.run("How many unread emails do I have? Also tell me if I have any.")
# Returns: {'count': 100, 'has_unread': True}

# Agent works with message attributes directly
agent.run("Search for emails from john@example.com and show me the subjects")
# Agent accesses: [msg['subject'] for msg in search_results['messages']]
```

**Performance comparison:**
- **Script version**: 24.49s total (1.37s model load + 23.11s processing)
- **Server version**: ~2s after initial load (saves ~22s per request)

The local model orchestrator (GPT-5-nano) efficiently routes to powerful Gmail tools while keeping costs minimal!