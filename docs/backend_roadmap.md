
# 🏗️ Backend Roadmap & Gap Analysis

> **Version:** 1.0.0
> **Date:** 2026-02-02
> **Focus:** Backend Hardening, Scalability, and Security

## 📊 Current State Analysis (v0.2.0)

The backend has successfully migrated to a **Hexagonal Architecture** with **Multi-Interface** support (FastAPI + MCP).

| Metric | Status | Notes |
| :--- | :--- | :--- |
| **Architecture** | ✅ Hexagonal | Ports & Adapters fully implemented. Domain isolated. |
| **Test Coverage** | ⚠️ ~90% | Core domain/application covered. Gaps in legacy CLI and server entrypoint. |
| **LLM Support** | ✅ Multi-Provider | Gemini, Ollama, LM Studio supported via Factory pattern. |
| **Interfaces** | ✅ Hybrid | REST API (FastAPI) + MCP (Claude Desktop). |
| **Persistence** | ⚠️ JSON File | `JsonFileRepository` is thread-safe but not scalable. |

---

## 🛑 Identified GAPS & Problems

### 1. Persistence & Scalability (Critical)

- **Current:** Single `batches.json` file.
- **Problem:**
  - High risk of corruption with concurrent writes (despite lock).
  - No query capabilities (filtering is done in-memory Python side).
  - Performance degrades linearly with file size (O(n) read/write).
- **Solution:** Migrate to **SQLite** (dev) / **PostgreSQL** (prod) with **SQLAlchemy 2.0**.

### 2. Concurrency & Blocking (High)

- **Current:** Async FastAPI, but CPU-bound tasks (future Audio analysis) will block.
- **Problem:** Python GIL limits concurrent request handling during intense processing.
- **Solution:** Implement **Celery** + **Redis** for task offloading (Asynchronous Task Queue).

### 3. Security (High)

- **Current:** Open API, no Authentication/Authorization.
- **Problem:** Anyone with network access can trigger LLM costs or batch operations.
- **Solution:** Implement **JWT Authentication** (OAuth2 with Bearer token).

### 4. Observability (Medium)

- **Current:** Basic `print` or standard logging.
- **Problem:** Impossible to trace request lifecycle across Adapters/LLMs.
- **Solution:** Structured implementation using `structlog` and **OpenTelemetry**.

### 5. Legacy Code (Low)

- **Current:** `src/adapters/input/cli/` contains old scripts.
- **Problem:** Confusing for new developers, potential for rot.
- **Solution:** Deprecate `maestro_cli.py` or refactor it to use `MaestroTools` properly.

---

## 🗺️ Backend Roadmap

### Phase 2.5: Stabilization (Current Focus)

- [x] Fix Unit Tests for MCP & UTCP Adapters (done).
- [ ] Refactor `main_server.py` integration tests for 100% coverage.
- [ ] Deprecate/Remove legacy CLI code.

### Phase 4: Backend Hardening (Post-Frontend)

1. **Database Migration**
    - [ ] Design Schema (Albums, Tracks, Batches, Users).
    - [ ] Implement `SqlAlchemyAdapter` (Ports & Adapters allows swapping `JsonFileRepository` easily).
    - [ ] Add Alembic for migrations.

2. **Security Layer**
    - [ ] Add `AuthService`.
    - [ ] Add API Key support for MCP.

3. **Task Queue**
    - [ ] Setup Redis container.
    - [ ] Move `MaestroTools.design_album` heavy lifting to Celery worker.

### Phase 5: Production Readiness

1. **Observability**
    - [ ] Add Correlation IDs.
    - [ ] Setup Prometheus metrics (request latency, LLM token usage).

2. **Deployment**
    - [ ] Optimization of Dockerfile (Multi-stage build).
    - [ ] CI/CD pipeline for automated PyPI/Docker Hub publishing.
