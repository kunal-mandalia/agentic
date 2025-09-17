# Running SmoLAgents with Local Models

## Overview
Using local models eliminates internet dependency and provides better privacy and control over your agentic system.

## Local Model Options

### 1. Ollama (Recommended)
Easy-to-use local model runner with many pre-built models.

#### Setup:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (examples)
ollama pull llama3.2:3b     # Small, fast model
ollama pull llama3.2:8b     # Balanced performance
ollama pull codellama:7b    # Code-focused model
ollama pull mistral:7b      # Alternative option

# Start Ollama server
ollama serve
```

#### Integration with SmoLAgents:
```python
from smolagents import CodeAgent, tool
import requests
import json

class OllamaLLM:
    def __init__(self, model="llama3.2:3b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, prompt):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

# Use with agent
llm = OllamaLLM()
agent = CodeAgent(tools=[], llm=llm)
```

### 2. llama.cpp
Direct integration with llama models.

#### Setup:
```bash
# Install llama-cpp-python
pip install llama-cpp-python

# Download a GGUF model file
# Example: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
```

#### Integration:
```python
from llama_cpp import Llama

llm = Llama(
    model_path="./models/phi-3-mini-4k-instruct-q4.gguf",
    n_ctx=2048,
    verbose=False
)

# Custom wrapper for SmoLAgents
class LlamaCppLLM:
    def __init__(self, model_path):
        self.llm = Llama(model_path=model_path, n_ctx=2048)

    def generate(self, prompt, max_tokens=512):
        output = self.llm(prompt, max_tokens=max_tokens)
        return output["choices"][0]["text"]
```

### 3. Transformers with Local Models
Using Hugging Face transformers library.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

class TransformersLLM:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def generate(self, prompt, max_length=512):
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## Model Recommendations

### For Learning (Small/Fast):
- **Phi-3 Mini (3.8B)**: Microsoft's efficient small model
- **Llama 3.2 3B**: Meta's latest small model
- **TinyLlama (1.1B)**: Ultra-lightweight for testing

### For Production (Balanced):
- **Llama 3.2 8B**: Good balance of size and capability
- **Mistral 7B**: Strong performance
- **CodeLlama 7B**: Code-focused tasks

### For Code Tasks:
- **CodeLlama**: Specialized for code generation
- **Phi-3**: Strong coding capabilities
- **DeepSeek Coder**: Code-specific model

## Hardware Requirements

| Model Size | RAM (Minimum) | RAM (Recommended) | Notes |
|------------|---------------|-------------------|-------|
| 1B-3B      | 4GB           | 8GB               | Fast, basic tasks |
| 7B-8B      | 8GB           | 16GB              | Balanced performance |
| 13B+       | 16GB          | 32GB              | High quality, slower |

## Performance Tips

1. **Use quantized models** (Q4, Q5) to reduce memory usage
2. **Adjust context length** based on your use case
3. **Use GPU acceleration** if available
4. **Batch requests** for efficiency
5. **Cache common responses** for repeated patterns

## Example: Complete Local Setup

```python
# requirements.txt additions
# ollama
# requests

from smolagents import tool
import subprocess
import os

@tool
def file_reader(filepath: str) -> str:
    """Read contents of a file"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

# Ensure Ollama is running
subprocess.run(["ollama", "serve"], check=False)

# Create agent with local model
agent = LocalAgent(
    tools=[file_reader],
    model="llama3.2:3b"  # Local Ollama model
)

# Test
result = agent.run("Read the README.md file and summarize it")
print(result)
```