# Simple Agent Examples

## Example 1: File Manager Agent

A basic agent that can read, write, and organize files.

### Tools Needed:
- `read_file`: Read file contents
- `write_file`: Write content to file
- `list_files`: List files in directory
- `search_files`: Search for files by pattern

### Sample Interactions:
- "Read the contents of README.md"
- "Create a new file called notes.txt with my meeting notes"
- "Show me all Python files in this directory"
- "Find all files containing 'TODO'"

## Example 2: Calculator Agent

A mathematical assistant that can perform calculations and explain steps.

### Tools Needed:
- `calculate`: Basic arithmetic operations
- `convert_units`: Unit conversions
- `format_number`: Number formatting

### Sample Interactions:
- "What is 25% of 480?"
- "Convert 32 degrees Celsius to Fahrenheit"
- "Calculate compound interest for $1000 at 5% for 3 years"

## Example 3: Text Processing Agent

An agent for text analysis and manipulation.

### Tools Needed:
- `count_words`: Word/character counting
- `summarize_text`: Text summarization
- `extract_keywords`: Keyword extraction
- `translate_text`: Language translation

### Sample Interactions:
- "Count the words in this document"
- "Summarize this article in 3 sentences"
- "Extract the main topics from this text"
- "Translate this paragraph to Spanish"

## Implementation Template

```python
from smolagents import CodeAgent, tool

# Define your tools
@tool
def your_tool(input_param: str) -> str:
    """Tool description for the agent"""
    # Implementation
    return result

# Create agent
agent = CodeAgent(
    tools=[your_tool],
    model="your-preferred-model"
)

# Use agent
response = agent.run("Your request here")
print(response)
```

## Best Practices

1. **Clear Tool Descriptions**: Help agent understand when to use each tool
2. **Error Handling**: Return helpful error messages
3. **Type Hints**: Use proper typing for parameters
4. **Simple Functions**: Keep tools focused on single tasks
5. **Testing**: Test tools individually before integrating