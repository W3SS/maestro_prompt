# MCP Server Configuration for Claude Desktop / Continue

This document explains how to integrate Maestro AI MCP Server with MCP clients.

## 🔧 LLM Provider Configuration

Maestro AI supports **3 LLM providers**:
1. **Gemini** (Google AI)
2. **Ollama** (Docker/Local)
3. **LM Studio** (Local OpenAI-compatible)

### Environment Variables

Create a `.env` file in the project root:

```bash
# LLM Provider Selection
LLM_PROVIDER=gemini  # Options: gemini | ollama | lmstudio

# Gemini Configuration (if using Gemini)
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Ollama Configuration (if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# LM Studio Configuration (if using LM Studio)
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL=local-model
```

---

## 🐳 Ollama Docker Setup

### 1. Start Ollama Container

```bash
# Pull and run Ollama
docker run -d --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama

# Pull a model (e.g., llama3)
docker exec -it ollama ollama pull llama3
```

### 2. Configure Maestro AI

```bash
# .env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

---

## 💻 LM Studio Setup

### 1. Start LM Studio Server

1. Open LM Studio
2. Load a model (e.g., Mistral, Llama)
3. Click "Local Server" tab
4. Start server (default: `http://localhost:1234`)

### 2. Configure Maestro AI

```bash
# .env
LLM_PROVIDER=lmstudio
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_MODEL=local-model
```

---

## 🔌 Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "maestro-ai": {
      "command": "python",
      "args": ["-m", "src.adapters.input.mcp.server"],
      "cwd": "h:/Meu Drive/codebase/tech/maestro_prompt",
      "env": {
        "LLM_PROVIDER": "ollama",
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "OLLAMA_MODEL": "llama3"
      }
    }
  }
}
```

**Change `LLM_PROVIDER` value to switch backends:**
- `"gemini"` - Google Gemini (requires API key)
- `"ollama"` - Ollama Docker/Local
- `"lmstudio"` - LM Studio Server

---

## 🧪 Testing

### Test MCP Server
```bash
python -m src.adapters.input.mcp.server
```

### Test Ollama Connection
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Hello, world!"
}'
```

### Test LM Studio Connection
```bash
curl http://localhost:1234/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "local-model",
  "messages": [{"role": "user", "content": "Hello!"}]
}'
```

---

## 📋 Available Tools (8 total)

### Album Design
- `design_album` - Generate concept album with AI

### Batch Management
- `create_batch` - Create new Suno batch
- `add_items_to_batch` - Add tracks to batch
- `get_batch` - Get batch details
- `list_batches` - List all batches (filterable)

### Batch Operations
- `start_batch` - Start processing
- `complete_batch` - Mark as completed
- `cancel_batch` - Cancel batch

---

## 🚨 Troubleshooting

### Ollama Connection Failed
```bash
# Check if Ollama is running
docker ps | grep ollama

# Check Ollama logs
docker logs ollama

# Test API
curl http://localhost:11434/api/tags
```

### LM Studio Connection Failed
- Verify LM Studio server is running
- Check port 1234 is not blocked
- Ensure a model is loaded

### Gemini API Key Issues
```bash
# Verify API key in .env
cat .env | grep GEMINI_API_KEY
```
