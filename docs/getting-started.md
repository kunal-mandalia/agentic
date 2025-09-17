# Getting Started with SmoLAgents

## Installation

```bash
pip install smolagents
```

## Basic Concepts

### Agent
The core component that processes requests and orchestrates tool usage.

### Tools
Functions that agents can call to perform specific tasks. Tools have:
- Name and description
- Input/output specifications
- Implementation logic

### Workflow
1. User provides input/request
2. Agent analyzes request
3. Agent selects appropriate tools
4. Agent executes tools in sequence
5. Agent returns result

## Minimal Example

```python
from smolagents import CodeAgent, tool

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

# Create agent with tool
agent = CodeAgent(tools=[calculator])

# Use the agent
result = agent.run("What is 15 * 7?")
print(result)
```

## Key Features to Explore

1. **Custom Tools**: Create domain-specific functions
2. **Multi-step Reasoning**: Chain multiple tool calls
3. **Context Management**: Maintain conversation history
4. **Error Handling**: Graceful failure recovery
5. **Tool Composition**: Combine simple tools for complex tasks

## Development Environment Setup

1. Create virtual environment
2. Install dependencies
3. Set up project structure
4. Configure logging and debugging
5. Write first agent