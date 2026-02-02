# Maestro AI - Neural Audio Workstation

> AI-powered album generation and batch management for Suno AI

## 📊 Project Status

- **Backend:** ✅ Phase 2 Complete (138/139 tests passing, 83% coverage)
- **Frontend:** 🔄 Phase 3 Planned (React SPA with UI designs ready)
- **Interfaces:** FastAPI (REST) + MCP (Claude Desktop)
- **LLM Support:** Gemini, Ollama, LM Studio

---

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

### API & Integration

- **OpenAPI/Swagger:** <http://localhost:8000/docs> (when running API mode)
- **ReDoc:** <http://localhost:8000/redoc>
- **MCP Setup Guide:** [`src/adapters/input/mcp/README.md`](src/adapters/input/mcp/README.md)

### Project Documentation

- **📖 Complete Walkthrough:** [`docs/walkthrough.md`](docs/walkthrough.md) - Full project history and implementation details
- **📋 Task Breakdown:** [`docs/task.md`](docs/task.md) - Current status and roadmap
- **🎨 Frontend Plan:** [`docs/frontend_plan.md`](docs/frontend_plan.md) - React SPA implementation plan
- **🏛️ Architecture:** [`docs/architecture.md`](docs/architecture.md) - Hexagonal architecture overview

### UI/UX Designs

- **🎭 Album Designer UI:** [`docs/designs/album_designer_ui.png`](docs/designs/album_designer_ui.png)
- **📦 Batch Manager UI:** [`docs/designs/batch_manager_ui.png`](docs/designs/batch_manager_ui.png)
- **📐 Design Specifications:** [`docs/designs/design_specs.md`](docs/designs/design_specs.md) - Complete design system

### Additional Resources

- **Integration Guides:** `docs/INTEGRATION_GUIDE.md`
- **Genre Fusion Analysis:** `docs/GENRE_FUSION_ANALYSIS.md`
- **Vocal Profiles:** `docs/VOCAL_PROFILES_ENHANCED_GUIDE.md`

## ✅ Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```
