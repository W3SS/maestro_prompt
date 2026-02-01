"""
Flask REST API for Maestro AI
Phase 1: Core API Foundation
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import uuid
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///maestro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class Album(db.Model):
    __tablename__ = 'albums'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    archetype = db.Column(db.String(100), nullable=False)
    narrative = db.Column(db.Text)
    num_tracks = db.Column(db.Integer, default=8)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tracks = db.relationship('Track', backref='album', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'archetype': self.archetype,
            'narrative': self.narrative,
            'num_tracks': self.num_tracks,
            'created_at': self.created_at.isoformat(),
            'tracks': [track.to_dict() for track in self.tracks]
        }

class Track(db.Model):
    __tablename__ = 'tracks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    album_id = db.Column(db.String(36), db.ForeignKey('albums.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.Text)
    genre = db.Column(db.String(100))
    mood = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    style_prompt = db.Column(db.Text)
    lyrics = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'album_id': self.album_id,
            'title': self.title,
            'theme': self.theme,
            'genre': self.genre,
            'mood': self.mood,
            'status': self.status,
            'style_prompt': self.style_prompt,
            'lyrics': self.lyrics,
            'created_at': self.created_at.isoformat()
        }

# ============================================================================
# API ENDPOINTS - ALBUMS
# ============================================================================

@app.route('/api/albums', methods=['GET'])
def get_albums():
    """List all albums"""
    albums = Album.query.order_by(Album.created_at.desc()).all()
    return jsonify([album.to_dict() for album in albums])

@app.route('/api/albums/<album_id>', methods=['GET'])
def get_album(album_id):
    """Get specific album by ID"""
    album = Album.query.get_or_404(album_id)
    return jsonify(album.to_dict())

@app.route('/api/albums/design', methods=['POST'])
def design_album():
    """Design a new album using Maestro AI"""
    data = request.get_json()
    
    # Validate input
    if not data.get('archetype'):
        return jsonify({'error': 'archetype is required'}), 400
    
    archetype = data['archetype']
    title = data.get('title')
    num_tracks = data.get('num_tracks', 8)
    
    # Import here to avoid circular dependency
    from maestro_ollama_enhanced import MaestroAlbumArchitect, MaestroDataLoader
    
    # Design album using Maestro
    data_loader = MaestroDataLoader()
    architect = MaestroAlbumArchitect(data_loader)
    
    # This will save to fila_suno_v2.csv
    csv_path = architect.design_album(archetype, title, num_tracks)
    
    if not csv_path:
        return jsonify({'error': 'Failed to design album'}), 500
    
    # Read the generated tracks from CSV
    import pandas as pd
    df = pd.read_csv(csv_path)
    
    # Get the last num_tracks rows (the ones we just added)
    recent_tracks = df.tail(num_tracks)
    
    # Create album in database
    album = Album(
        title=recent_tracks.iloc[0]['album'],
        archetype=archetype,
        narrative=recent_tracks.iloc[0].get('observacoes', ''),
        num_tracks=num_tracks
    )
    db.session.add(album)
    
    # Create tracks in database
    for _, row in recent_tracks.iterrows():
        track = Track(
            album_id=album.id,
            title=row['titulo'],
            theme=row['tema'],
            genre=row['genero'],
            mood=row['mood'],
            status='pending'
        )
        db.session.add(track)
    
    db.session.commit()
    
    return jsonify(album.to_dict()), 201

@app.route('/api/albums/<album_id>', methods=['DELETE'])
def delete_album(album_id):
    """Delete an album and all its tracks"""
    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    return '', 204

# ============================================================================
# API ENDPOINTS - TRACKS/SONGS
# ============================================================================

@app.route('/api/songs/queue', methods=['GET'])
def get_queue():
    """Get all pending tracks"""
    tracks = Track.query.filter_by(status='pending').order_by(Track.created_at).all()
    return jsonify([track.to_dict() for track in tracks])

@app.route('/api/songs/<track_id>', methods=['GET'])
def get_song(track_id):
    """Get specific track by ID"""
    track = Track.query.get_or_404(track_id)
    return jsonify(track.to_dict())

@app.route('/api/songs/<track_id>/status', methods=['PATCH'])
def update_song_status(track_id):
    """Update track status"""
    track = Track.query.get_or_404(track_id)
    data = request.get_json()
    
    if 'status' in data:
        track.status = data['status']
    if 'style_prompt' in data:
        track.style_prompt = data['style_prompt']
    if 'lyrics' in data:
        track.lyrics = data['lyrics']
    
    db.session.commit()
    return jsonify(track.to_dict())

@app.route('/api/songs/generate', methods=['POST'])
def generate_songs():
    """
    Generate songs from queue (async via Celery in production)
    For now, returns task info
    """
    data = request.get_json()
    track_ids = data.get('track_ids', [])
    
    if not track_ids:
        # Generate all pending tracks
        tracks = Track.query.filter_by(status='pending').all()
        track_ids = [t.id for t in tracks]
    
    # In production, this would dispatch to Celery
    # For now, just mark as processing
    for track_id in track_ids:
        track = Track.query.get(track_id)
        if track:
            track.status = 'processing'
    
    db.session.commit()
    
    return jsonify({
        'message': f'Started generation for {len(track_ids)} tracks',
        'track_ids': track_ids
    }), 202

# ============================================================================
# API ENDPOINTS - METADATA
# ============================================================================

@app.route('/api/archetypes', methods=['GET'])
def get_archetypes():
    """List all available archetypes"""
    from maestro_ollama_enhanced import MaestroDataLoader
    
    data_loader = MaestroDataLoader()
    archetypes = data_loader.aesthetics_semiotics.get('pop_culture_archetypes', {})
    
    result = []
    for key, value in archetypes.items():
        result.append({
            'id': key,
            'directorial_tone': value.get('directorial_tone'),
            'sonic_palette': value.get('sonic_palette', []),
            'lyrical_themes': value.get('lyrical_themes', [])
        })
    
    return jsonify(result)

@app.route('/api/archetypes/<archetype_id>', methods=['GET'])
def get_archetype(archetype_id):
    """Get specific archetype details"""
    from maestro_ollama_enhanced import MaestroDataLoader
    
    data_loader = MaestroDataLoader()
    archetypes = data_loader.aesthetics_semiotics.get('pop_culture_archetypes', {})
    
    if archetype_id not in archetypes:
        return jsonify({'error': 'Archetype not found'}), 404
    
    return jsonify({
        'id': archetype_id,
        **archetypes[archetype_id]
    })

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("✅ Database initialized!")

@app.cli.command()
def reset_db():
    """Reset the database (WARNING: deletes all data)"""
    db.drop_all()
    db.create_all()
    print("✅ Database reset!")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
