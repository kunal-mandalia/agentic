# Local Model Configuration Examples

## Quick Start: Ollama Setup

### 1. Install and Setup Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Pull a model (choose based on your hardware)
ollama pull llama3.2:3b    # Lightweight (4GB RAM)
ollama pull llama3.2:8b    # Balanced (8GB RAM)
ollama pull codellama:7b   # Code-focused (8GB RAM)
```

### 2. Test Ollama is Working
```bash
ollama run llama3.2:3b
# Type a message to test, then exit with /bye
```

## Complete Working Examples

### Example 1: File Manager Agent with Local Model

```python
# file_manager_agent.py
from smolagents import CodeAgent, tool
import requests
import os
import json
from pathlib import Path

class OllamaLLM:
    def __init__(self, model="llama3.2:3b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, prompt, **kwargs):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {e}"

@tool
def read_file(filepath: str) -> str:
    """Read the contents of a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"File content of {filepath}:\n{content}"
    except Exception as e:
        return f"Error reading file {filepath}: {e}"

@tool
def list_files(directory: str = ".") -> str:
    """List files in a directory"""
    try:
        path = Path(directory)
        if not path.exists():
            return f"Directory {directory} does not exist"

        files = []
        for item in path.iterdir():
            if item.is_file():
                files.append(f"📄 {item.name}")
            elif item.is_dir():
                files.append(f"📁 {item.name}/")

        return f"Contents of {directory}:\n" + "\n".join(files)
    except Exception as e:
        return f"Error listing directory {directory}: {e}"

@tool
def write_file(filepath: str, content: str) -> str:
    """Write content to a file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote content to {filepath}"
    except Exception as e:
        return f"Error writing to file {filepath}: {e}"

# Create the agent
def create_file_manager():
    llm = OllamaLLM()
    tools = [read_file, list_files, write_file]
    return CodeAgent(tools=tools, llm=llm)

if __name__ == "__main__":
    agent = create_file_manager()

    # Test the agent
    print("File Manager Agent Ready!")
    print("Example commands:")
    print("- 'List all files in the current directory'")
    print("- 'Read the README.md file'")
    print("- 'Create a new file called notes.txt with some example content'")

    while True:
        user_input = input("\n> ")
        if user_input.lower() in ['quit', 'exit']:
            break

        try:
            result = agent.run(user_input)
            print(f"\n{result}")
        except Exception as e:
            print(f"Error: {e}")
```

### Example 2: Calculator Agent with Error Handling

```python
# calculator_agent.py
from smolagents import CodeAgent, tool
import requests
import math
import re

class OllamaLLM:
    def __init__(self, model="llama3.2:3b"):
        self.model = model
        self.base_url = "http://localhost:11434"

    def generate(self, prompt, **kwargs):
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            return response.json()["response"]
        except Exception as e:
            return f"Error: {e}"

@tool
def calculate(expression: str) -> str:
    """Safely evaluate mathematical expressions"""
    # Remove any non-math characters for safety
    allowed_chars = set('0123456789+-*/().^ ')
    if not all(c in allowed_chars for c in expression.replace(' ', '')):
        return "Error: Invalid characters in expression"

    # Replace ^ with ** for Python
    expression = expression.replace('^', '**')

    try:
        # Use eval safely with limited builtins
        allowed_names = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "pow": pow,
            "max": max,
            "min": min,
        }
        result = eval(expression, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {e}"

@tool
def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Convert to Celsius first
    if from_unit == 'fahrenheit' or from_unit == 'f':
        celsius = (value - 32) * 5/9
    elif from_unit == 'kelvin' or from_unit == 'k':
        celsius = value - 273.15
    elif from_unit == 'celsius' or from_unit == 'c':
        celsius = value
    else:
        return f"Unknown temperature unit: {from_unit}"

    # Convert from Celsius to target
    if to_unit == 'fahrenheit' or to_unit == 'f':
        result = celsius * 9/5 + 32
        unit_name = "Fahrenheit"
    elif to_unit == 'kelvin' or to_unit == 'k':
        result = celsius + 273.15
        unit_name = "Kelvin"
    elif to_unit == 'celsius' or to_unit == 'c':
        result = celsius
        unit_name = "Celsius"
    else:
        return f"Unknown temperature unit: {to_unit}"

    return f"{value}° {from_unit.title()} = {result:.2f}° {unit_name}"

# Create and run the agent
def main():
    llm = OllamaLLM()
    agent = CodeAgent(tools=[calculate, convert_temperature], llm=llm)

    print("Calculator Agent Ready!")
    print("Try: 'What is 25 * 4 + 10?' or 'Convert 32 Fahrenheit to Celsius'")

    while True:
        user_input = input("\n> ")
        if user_input.lower() in ['quit', 'exit']:
            break

        result = agent.run(user_input)
        print(f"\n{result}")

if __name__ == "__main__":
    main()
```

## Configuration Tips

### Model Selection by Hardware

```python
# config.py
import psutil

def get_recommended_model():
    """Recommend model based on available RAM"""
    memory_gb = psutil.virtual_memory().total / (1024**3)

    if memory_gb >= 16:
        return "llama3.2:8b"  # Better quality
    elif memory_gb >= 8:
        return "llama3.2:3b"  # Balanced
    else:
        return "phi3:mini"    # Lightweight

def create_llm():
    model = get_recommended_model()
    print(f"Using model: {model}")
    return OllamaLLM(model=model)
```

### Environment Variables

```python
# .env file
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
DEFAULT_MODEL=llama3.2:3b
```

```python
# config with env vars
import os
from dotenv import load_dotenv

load_dotenv()

class OllamaLLM:
    def __init__(self):
        host = os.getenv('OLLAMA_HOST', 'localhost')
        port = os.getenv('OLLAMA_PORT', '11434')
        self.model = os.getenv('DEFAULT_MODEL', 'llama3.2:3b')
        self.base_url = f"http://{host}:{port}"
```

## Troubleshooting

### Common Issues

1. **Ollama not running**:
   ```bash
   ollama serve
   ```

2. **Model not found**:
   ```bash
   ollama list  # Check available models
   ollama pull llama3.2:3b  # Pull if missing
   ```

3. **Connection timeout**:
   ```python
   # Increase timeout in requests
   response = requests.post(..., timeout=60)
   ```

4. **Memory issues**:
   - Use smaller model (phi3:mini)
   - Reduce context window
   - Close other applications

### Performance Monitoring

```python
import time
import psutil

def monitor_performance():
    start_time = time.time()
    start_memory = psutil.virtual_memory().used / (1024**2)

    # Your agent code here

    end_time = time.time()
    end_memory = psutil.virtual_memory().used / (1024**2)

    print(f"Time: {end_time - start_time:.2f}s")
    print(f"Memory used: {end_memory - start_memory:.0f}MB")
```