# Maestro AI - Quick Start Guide

## 🚀 Running the Full Stack

### Backend (Flask API)

```bash
# Install dependencies
pip install -r requirements-web.txt

# Initialize database
python app.py

# In another terminal, run the Flask server
python app.py
```

API will be available at `http://localhost:5000`

### Frontend (React)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Ollama (Docker)

```bash
# Start Ollama
docker-compose up -d

# Pull model (first time only)
docker exec -it maestro_ollama ollama pull mistral-nemo:12b
```

## 📡 API Endpoints

### Albums

* `GET /api/albums` - List all albums
* `GET /api/albums/{id}` - Get album details
* `POST /api/albums/design` - Design new album
* `DELETE /api/albums/{id}` - Delete album

### Songs

* `GET /api/songs/queue` - Get pending tracks
* `GET /api/songs/{id}` - Get track details
* `POST /api/songs/generate` - Start generation
* `PATCH /api/songs/{id}/status` - Update track status

### Metadata

* `GET /api/archetypes` - List all archetypes
* `GET /api/archetypes/{id}` - Get archetype details

## 🎨 Frontend Pages

1. **Dashboard** (`/`) - Overview with stats and recent albums
2. **Album Designer** (`/design`) - Create new albums with archetype selection
3. **Queue Viewer** (`/queue`) - View and manage pending tracks

## 🐳 Docker Deployment

```bash
# Build and run everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Environment Variables

Create `.env` file:

```env
DATABASE_URL=sqlite:///maestro.db
SECRET_KEY=your-secret-key-here
OLLAMA_URL=http://localhost:11434
```

## 📝 Next Steps

1. Add authentication (JWT)
2. Implement WebSocket for real-time updates
3. Add Celery for background tasks
4. Deploy to production (Heroku/Railway/Fly.io)
