# Multi-Language Setup Guide

## Quick Start

Choose your preferred language and follow the corresponding setup:

```bash
# Clone and enter the repository
git clone <your-repo>
cd agentic

# Setup your chosen language
./scripts/setup.sh python     # Python with UV
./scripts/setup.sh javascript # Node.js with npm
./scripts/setup.sh all        # Both languages
```

## Python Setup (`/python/`)

### Prerequisites
- Python 3.11+
- UV package manager

### Installation
```bash
cd python/

# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Install local model support (optional)
uv add --optional local-models

# Setup Ollama for local models
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:3b
```

### Running Python Examples
```bash
# Basic calculator agent
uv run examples/basic_calculator.py

# File manager agent
uv run examples/file_organizer.py

# Interactive mode
uv run -m agentic.cli
```

### Python Development
```bash
# Run tests
uv run pytest

# Format code
uv run black src/ examples/ tests/

# Lint code
uv run ruff check src/ examples/ tests/

# Type checking
uv run mypy src/
```

## JavaScript Setup (`/javascript/`)

### Prerequisites
- Node.js 18+
- npm, yarn, or pnpm

### Installation
```bash
cd javascript/

# Install dependencies
npm install

# Or with yarn
yarn install

# Or with pnpm
pnpm install

# Setup environment
cp .env.example .env
```

### Running JavaScript Examples
```bash
# Basic calculator agent
npm run example:calculator

# File manager agent
npm run example:file-manager

# Interactive CLI
npm start
```

### JavaScript Development
```bash
# Run tests
npm test

# Watch mode for development
npm run dev

# Format code
npm run format

# Lint code
npm run lint

# Type checking (if using TypeScript)
npm run type-check
```

## Local Model Setup

### Ollama (Recommended)
Works with both Python and JavaScript:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve &

# Pull models based on your hardware
ollama pull llama3.2:3b      # 4GB+ RAM
ollama pull llama3.2:8b      # 8GB+ RAM
ollama pull codellama:7b     # Code-focused
ollama pull mistral:7b       # Alternative option

# Test it's working
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.2:3b", "prompt": "Hello!", "stream": false}'
```

### Hardware Requirements
| Model | RAM | Speed | Use Case |
|-------|-----|-------|----------|
| llama3.2:3b | 4GB+ | Fast | Learning, basic tasks |
| llama3.2:8b | 8GB+ | Balanced | General purpose |
| codellama:7b | 8GB+ | Medium | Code tasks |
| mistral:7b | 8GB+ | Medium | Advanced reasoning |

## Docker Setup

### Single Language Container
```bash
# Python container
cd python/
docker build -t agentic-python .
docker run -it --network host agentic-python

# JavaScript container
cd javascript/
docker build -t agentic-js .
docker run -it --network host agentic-js
```

### Multi-Language with Docker Compose
```bash
# From repository root
docker-compose up

# Development mode with hot reload
docker-compose -f docker-compose.dev.yml up

# Scale specific services
docker-compose up --scale python-agent=2
```

## Environment Configuration

### Shared Environment Variables
Create `.env` files in each language directory:

```bash
# Model Configuration
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
DEFAULT_MODEL=llama3.2:3b

# Agent Settings
MAX_ITERATIONS=10
TIMEOUT_SECONDS=30
CONTEXT_WINDOW=2048

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# API Keys (if using cloud models)
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

### Language-Specific Configuration

**Python** (`python/.env`):
```bash
# Python-specific
PYTHONPATH=src
UV_CACHE_DIR=.uv-cache

# Model paths
MODELS_DIR=../shared/models
PROMPTS_DIR=../shared/prompts
```

**JavaScript** (`javascript/.env`):
```bash
# Node.js-specific
NODE_ENV=development
NODE_OPTIONS=--max-old-space-size=4096

# Model paths
MODELS_DIR=../shared/models
PROMPTS_DIR=../shared/prompts
```

## Validation Scripts

### Check Environment
```bash
# Run from repository root
./scripts/check-environment.sh

# Check specific language
./scripts/check-environment.sh python
./scripts/check-environment.sh javascript
```

### Test Setup
```bash
# Test all languages
./scripts/test-setup.sh

# Test specific components
./scripts/test-setup.sh ollama
./scripts/test-setup.sh python-deps
./scripts/test-setup.sh js-deps
```

## Development Workflow

### Working Across Languages

1. **Start with one language**: Choose Python or JavaScript
2. **Set up local models**: Install Ollama and pull a model
3. **Run examples**: Test basic functionality
4. **Implement agents**: Create your first custom agent
5. **Compare implementations**: Try the same agent in both languages
6. **Optimize**: Profile and improve performance

### Common Tasks

```bash
# Format all code
./scripts/format-all.sh

# Run all tests
./scripts/test-all.sh

# Benchmark performance
./scripts/benchmark-all.sh

# Update dependencies
./scripts/update-deps.sh
```

## Troubleshooting

### Common Issues

**Ollama Connection Error**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

**Memory Issues**:
```bash
# Use smaller model
ollama pull llama3.2:3b

# Monitor memory usage
htop
```

**Python UV Issues**:
```bash
# Clear UV cache
uv cache clean

# Reinstall dependencies
rm uv.lock && uv sync
```

**Node.js Issues**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules && npm install
```

### Getting Help

1. **Check language-specific READMEs**: `python/README.md`, `javascript/README.md`
2. **Review examples**: Start with working code in `examples/`
3. **Run validation scripts**: `./scripts/check-environment.sh`
4. **Check model compatibility**: Ensure your hardware supports the chosen model

## Next Steps

After setup:
1. **Follow getting-started.md**: Language-agnostic concepts
2. **Try examples**: Run pre-built agents
3. **Read comparisons.md**: Understand language tradeoffs
4. **Build your first agent**: Start with calculator or file manager
5. **Contribute**: Add new languages or improve existing ones