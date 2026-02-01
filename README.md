# Maestro AI - Quick Start Guide

## 🚀 Installation

```bash
# Clone repository
git clone <repo-url>
cd maestro_prompt

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your LLM provider settings
```

## 🎮 Usage

### Option 1: FastAPI Server (HTTP REST)

```bash
python -m src.main_server --mode api

# Visit: http://localhost:8000/docs
```

**Endpoints:**
- `POST /album/design` - Generate album with AI
- `POST /batch` - Create Suno batch
- `GET /batches` - List batches
- (5 more endpoints - see Swagger docs)

### Option 2: MCP Server (Claude Desktop / Continue)

```bash
python -m src.main_server --mode mcp
```

**Configure Claude Desktop:**
Edit `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "maestro-ai": {
      "command": "python",
      "args": ["-m", "src.main_server", "--mode", "mcp"],
      "cwd": "/path/to/maestro_prompt"
    }
  }
}
```

### Option 3: Both Servers

```bash
python -m src.main_server --mode all
```

## 🎨 LLM Providers

**Gemini (Default):**
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
```

**Ollama (Docker):**
```bash
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec -it ollama ollama pull llama3

LLM_PROVIDER=ollama
```

**LM Studio:**
```bash
# 1. Start LM Studio server
# 2. Set in .env:
LLM_PROVIDER=lmstudio
```

## 📚 Documentation

- **API Docs:** http://localhost:8000/docs
- **MCP Setup:** `src/adapters/input/mcp/README.md`
- **Architecture:** `architecture.md`
- **Walkthrough:** `walkthrough.md`

## ✅ Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```
