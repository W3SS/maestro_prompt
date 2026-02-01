# Maestro AI - Neural Audio Workstation

> **Transform music creation with AI-powered album design using local LLMs and Test-Driven Development**

[![CI](https://github.com/W3SS/maestro_prompt/actions/workflows/ci.yml/badge.svg)](https://github.com/W3SS/maestro_prompt/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-35%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-98.6%25-brightgreen.svg)](htmlcov/)
[![Architecture](https://img.shields.io/badge/architecture-hexagonal-purple.svg)](#architecture)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

## 🎯 Vision

Maestro AI desconstructs and reconstructs complex music (Metal/Jazz/IDM) by combining native stability with local generative AI, running efficiently on modest hardware (Intel 8th Gen, 8GB RAM).

## ✨ Features

### ✅ Phase 1: Stability & CLI (Completed)

- **🔄 LLM Client**: Async Ollama client with configurable timeout (1300s for 12b models), exponential backoff (3 retries), and connection pooling
- **📦 Context Manager**: Smart JSON loading with 60% payload reduction and TTL-based caching
- **🏗️ Hexagonal Architecture**: Clean separation between domain, application, and infrastructure layers
- **✅ Test Coverage**: 91% coverage with 30 unit tests (TDD approach)

### 📋 Phase 2: Web App (Planned)

- [ ] Flask REST API with SQLAlchemy
- [ ] React + Vite frontend with Tailwind CSS
- [ ] Celery + Redis for async task queue
- [ ] Real-time WebSocket updates

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (for Ollama)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/W3SS/maestro_prompt.git
cd maestro_prompt

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama via Docker
docker-compose up -d

# Download model (first time)
docker exec -it maestro_ollama ollama pull mistral-nemo:12b
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_llm_client.py -v
```

## � Project Structure (Hexagonal Architecture)

```
maestro_prompt/
├── src/
│   ├── domain/                    # Business logic (pure Python)
│   ├── application/               # Use cases & services
│   ├── ports/                     # Interfaces
│   │   ├── input/                 # Driving ports (CLI, API)
│   │   └── output/                # Driven ports (LLM, DB, File System)
│   ├── adapters/                  # Implementations
│   │   ├── input/cli/             # Command-line interface
│   │   └── output/                # External integrations
│   │       ├── llm/               # Ollama adapter
│   │       ├── context/           # JSON context loader
│   │       └── validation/        # Pydantic validators
│   └── infrastructure/            # Config, DI container
├── tests/
│   ├── unit/                      # Fast, isolated tests
│   └── integration/               # Tests with real dependencies
├── data/                          # JSON knowledge base
└── docs/                          # Documentation
```

### Architecture Benefits

| Benefit |  Description |
|---------|--------------|
| **Testability** | Domain/Application layers easily mocked |
| **Flexibility** | Swap Ollama for OpenAI? Just create new adapter |
| **Maintainability** | Changes in adapters don't affect core logic |
| **Scalability** | Add Flask API? Create new input adapter |

See [architecture.md](docs/architecture.md) for details.

## 🧪 Test-Driven Development

This project follows strict TDD (RED-GREEN-REFACTOR):

### Metrics

| Metric | Value |
|--------|-------|
| Total Tests | 37 |
| Passed | 35 |
| Skipped | 2 |
| Coverage | 98.63% |
| Test/Code Ratio | 1.5:1 |

See [TDD_REPORT.md](docs/TDD_REPORT.md) for development journey.

## 🔧 Configuration

### LLM Model

Edit timeout based on model size:

```python
# For 8b models
config = LLMConfig(model="llama3:8b", timeout=300)

# For 12b models (default)
config = LLMConfig(model="mistral-nemo:12b", timeout=1300)
```

### Context Caching

```python
# Disable cache (always reload)
context_config = ContextConfig(cache_enabled=False)

# Custom TTL (default: 1 hour)
context_config = ContextConfig(cache_ttl=7200)  # 2 hours
```

## 📚 Documentation

- [Architecture Guide](docs/architecture.md) - Hexagonal architecture explained
- [TDD Report](docs/TDD_REPORT.md) - Development journey with TDD
- [Implementation Plan](docs/implementation_plan.md) - Full roadmap
- [Task Tracking](docs/task.md) - Current progress

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Write tests first (TDD!)
4. Commit changes (`git commit -m 'feat: Add AmazingFeature'`)
5. Push to branch (`git push origin feature/AmazingFeature`)
6. Open Pull Request

### Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Adding tests
- `refactor:` Code restructuring

## 📝 License

This project is under the MIT License.

## 🙏 Acknowledgments

- **Ollama** - Local LLM inference
- **Suno.ai** - Music generation platform
- **Mistral AI** - Mistral-Nemo model

---

**Built with ❤️ using Test-Driven Development and Clean Architecture**
