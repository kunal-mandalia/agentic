# Smolagents Basic Implementation

A minimal implementation of smolagents demonstrating local model orchestration with powerful tools.

## Architecture

This project demonstrates using a lightweight model (GPT-5-nano) as an orchestrator to control specialized tools, providing:
- **Cost-effective** - Cheap model handles routing/orchestration
- **Fast** - No heavy model loading for basic decisions
- **Scalable** - Add tools incrementally for specific use cases

## Files

- `main.py` - Script version (loads model each run)
- `server.py` - Server version (loads model once, handles multiple requests)

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

# Add OpenAI API key to .env
echo "OPENAI_API_KEY=your-key-here" > .env

# Run script version
uv run python main.py

# Run server version
uv run python server.py
# Test: curl -X POST http://localhost:5000/run -H 'Content-Type: application/json' -d '{"task": "tell me a joke"}'
```

## Tools

Current tools:
- `calculator(a, b)` - Add two numbers
- `tell_joke()` - Returns a random joke

Extend by adding more `@tool` decorated functions for your specific use case.