"""Data Transfer Objects for Application layer."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class TrackDTO:
    """DTO for Track data transfer."""
    title: str
    lyrics: str
    style_tags: List[str]
    duration_estimate: Optional[int] = None
    track_number: int = 1


@dataclass
class AlbumDTO:
    """DTO for Album data transfer."""
    title: str
    archetype: str
    genres: List[str]
    tracks: List[TrackDTO] = field(default_factory=list)
    created_at: Optional[datetime] = None
    id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "archetype": self.archetype,
            "genres": self.genres,
            "tracks": [
                {
                    "title": t.title,
                    "lyrics": t.lyrics,
                    "style_tags": t.style_tags,
                    "duration_estimate": t.duration_estimate,
                    "track_number": t.track_number
                }
                for t in self.tracks
            ],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "id": self.id
        }


@dataclass
class BatchItemDTO:
    """DTO for BatchItem data transfer."""
    prompt: str
    style_tags: str
    title: str = ""
    status: str = "pending"
    suno_id: Optional[str] = None
    audio_url: Optional[str] = None


@dataclass
class BatchDTO:
    """DTO for Batch data transfer."""
    name: str
    items: List[BatchItemDTO] = field(default_factory=list)
    status: str = "pending"
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "status": self.status,
            "items": [
                {
                    "prompt": i.prompt,
                    "style_tags": i.style_tags,
                    "title": i.title,
                    "status": i.status,
                    "suno_id": i.suno_id,
                    "audio_url": i.audio_url
                }
                for i in self.items
            ],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "id": self.id,
            "metadata": self.metadata
        }
