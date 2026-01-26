# Flask Web App Roadmap

## Vision

Transform Maestro AI into a full-featured web application with REST API, real-time queue management, and collaborative album design.

## Phase 1: REST API Foundation

### Core Endpoints

#### Album Management

```
POST   /api/albums/design
GET    /api/albums
GET    /api/albums/{id}
DELETE /api/albums/{id}
```

#### Song Generation

```
POST   /api/songs/generate
GET    /api/songs/queue
GET    /api/songs/{id}
PATCH  /api/songs/{id}/status
```

#### Archetypes & Data

```
GET    /api/archetypes
GET    /api/archetypes/{id}
GET    /api/genres
GET    /api/moods
```

### Technology Stack

* **Backend**: Flask + Flask-RESTful
* **Database**: SQLite (dev) → PostgreSQL (prod)
* **ORM**: SQLAlchemy
* **Task Queue**: Celery + Redis (for async LLM calls)
* **API Docs**: Flask-RESTX (Swagger UI)

### Example Request

```json
POST /api/albums/design
{
  "archetype": "cosmic_horror",
  "title": "Echoes from the Abyss",
  "num_tracks": 8,
  "genres": ["Dark Ambient", "Post-Metal", "Drone-Doom"]
}
```

### Example Response

```json
{
  "id": "abc123",
  "title": "Echoes from the Abyss",
  "archetype": "cosmic_horror",
  "tracks": [
    {
      "id": "track001",
      "title": "Stellar Whispers",
      "genre": "Dark Ambient",
      "mood": "Anticipation",
      "status": "pending"
    }
  ],
  "created_at": "2026-01-25T16:00:00Z"
}
```

## Phase 2: Frontend Interface

### Technology Options

#### Option A: React SPA

* **Pros**: Rich interactivity, component reusability
* **Cons**: Requires build step, more complex setup
* **Stack**: React + Vite + TailwindCSS

#### Option B: Flask Templates (Jinja2)

* **Pros**: Simpler deployment, server-side rendering
* **Cons**: Less interactive, harder to scale
* **Stack**: Flask + Jinja2 + HTMX + AlpineJS

### Recommended: React SPA

```
src/
├── components/
│   ├── AlbumDesigner.jsx
│   ├── QueueViewer.jsx
│   ├── SongGenerator.jsx
│   └── ArchetypeSelector.jsx
├── pages/
│   ├── Dashboard.jsx
│   ├── Albums.jsx
│   └── Settings.jsx
├── services/
│   └── api.js
└── App.jsx
```

### Key Features

1. **Album Designer**
   * Archetype browser with search/filter
   * Real-time track preview
   * Genre diversity visualizer

2. **Queue Dashboard**
   * Live progress tracking
   * WebSocket updates for generation status
   * Drag-and-drop track reordering

3. **Song Editor**
   * Inline lyrics editing
   * Style prompt customization
   * A/B testing for different prompts

4. **Export Manager**
   * One-click Suno JSON export
   * Batch download lyrics as Markdown
   * Integration with Suno API (future)

## Phase 3: Advanced Features

### 1. User Authentication

* OAuth2 (Google, GitHub)
* JWT-based sessions
* Role-based access (Admin, Creator, Viewer)

### 2. Collaborative Albums

* Multi-user album design
* Track assignment and review
* Comment threads on tracks

### 3. AI Model Management

* Model selection UI (Llama 3, Mistral, etc.)
* Temperature/creativity sliders
* Prompt template library

### 4. Analytics Dashboard

* Genre distribution charts
* Mood correlation heatmaps
* Generation success rates

### 5. Integration Hub

* Suno API direct upload
* Spotify playlist export
* YouTube Music metadata sync

## Implementation Timeline

### Month 1: API Foundation

- [ ] Flask app structure
* [ ] SQLAlchemy models
* [ ] Core CRUD endpoints
* [ ] Celery task queue

### Month 2: Frontend MVP

- [ ] React project setup
* [ ] Album designer UI
* [ ] Queue viewer
* [ ] API integration

### Month 3: Polish & Deploy

- [ ] Authentication system
* [ ] WebSocket real-time updates
* [ ] Docker deployment
* [ ] CI/CD pipeline

## Deployment Architecture

```
┌─────────────────┐
│   Nginx Proxy   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│ React │ │  Flask  │
│  SPA  │ │   API   │
└───────┘ └────┬────┘
               │
        ┌──────┴──────┐
        │             │
   ┌────▼────┐  ┌────▼────┐
   │  Redis  │  │ Ollama  │
   │ (Queue) │  │  (LLM)  │
   └─────────┘  └─────────┘
```

## Database Schema

```sql
CREATE TABLE albums (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    archetype VARCHAR(100),
    narrative TEXT,
    created_at TIMESTAMP,
    user_id UUID
);

CREATE TABLE tracks (
    id UUID PRIMARY KEY,
    album_id UUID REFERENCES albums(id),
    title VARCHAR(255),
    theme TEXT,
    genre VARCHAR(100),
    mood VARCHAR(50),
    status VARCHAR(20),
    style_prompt TEXT,
    lyrics TEXT,
    created_at TIMESTAMP
);

CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    created_at TIMESTAMP
);
```

## Security Considerations

1. **API Rate Limiting**: 100 requests/minute per user
2. **Input Validation**: Pydantic schemas for all endpoints
3. **CORS**: Whitelist frontend domain only
4. **Secrets Management**: Environment variables + Vault
5. **SQL Injection**: SQLAlchemy ORM (no raw queries)

## Monitoring & Observability

* **Logging**: Structured JSON logs (ELK stack)
* **Metrics**: Prometheus + Grafana
* **Tracing**: OpenTelemetry
* **Alerts**: PagerDuty for critical failures

## Cost Estimation (Monthly)

| Service | Cost |
|---------|------|
| VPS (4 vCPU, 16GB RAM) | $40 |
| PostgreSQL (managed) | $15 |
| Redis (managed) | $10 |
| Domain + SSL | $2 |
| **Total** | **$67/month** |

## Next Steps

1. Review this roadmap with stakeholders
2. Set up Flask project structure
3. Design database schema in detail
4. Create API specification (OpenAPI 3.0)
5. Build MVP frontend mockups

---

*Last updated: 2026-01-25*
