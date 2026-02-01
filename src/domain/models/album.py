"""Domain models for Maestro AI - Album entity."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum

from src.domain.exceptions.domain_errors import (
    InvalidAlbumError,
    InvalidArchetypeError,
    InvalidGenreError
)


class Archetype(str, Enum):
    """Album archetypes - narrative themes."""
    COSMIC_HORROR = "cosmic_horror"
    DYSTOPIAN_REBELLION = "dystopian_rebellion"
    COLLEGE_COMING_OF_AGE = "college_coming_of_age"
    ROMANTIC_TRAGEDY = "romantic_tragedy"
    EPIC_FANTASY = "epic_fantasy"
    NOIR_DETECTIVE = "noir_detective"


class Genre(str, Enum):
    """Musical genres."""
    METAL = "metal"
    JAZZ = "jazz"
    PROGRESSIVE_ROCK = "progressive_rock"
    ELECTRONIC = "electronic"
    FOLK = "folk"
    CLASSICAL = "classical"
    FUSION = "fusion"


@dataclass
class Track:
    """Track entity - represents a song in an album."""
    title: str
    lyrics: str
    style_tags: List[str]
    duration_estimate: Optional[int] = None  # seconds
    track_number: int = 1
    
    def __post_init__(self):
        """Validate track data."""
        if not self.title or not self.title.strip():
            from src.domain.exceptions.domain_errors import InvalidTrackError
            raise InvalidTrackError("Track title cannot be empty")
        
        if not self.lyrics or not self.lyrics.strip():
            from src.domain.exceptions.domain_errors import InvalidTrackError
            raise InvalidTrackError("Track lyrics cannot be empty")
        
        if self.track_number < 1:
            from src.domain.exceptions.domain_errors import InvalidTrackError
            raise InvalidTrackError("Track number must be >= 1")
        
        if self.duration_estimate is not None and self.duration_estimate < 0:
            from src.domain.exceptions.domain_errors import InvalidTrackError
            raise InvalidTrackError("Duration must be positive")


@dataclass
class Album:
    """Album entity - aggregate root."""
    title: str
    archetype: Archetype
    genres: List[Genre]
    tracks: List[Track] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    id: Optional[str] = None
    
    def __post_init__(self):
        """Validate album data."""
        # Validate title
        if not self.title or not self.title.strip():
            raise InvalidAlbumError("Album title cannot be empty")
        
        # Validate archetype
        if not isinstance(self.archetype, Archetype):
            try:
                self.archetype = Archetype(self.archetype)
            except ValueError:
                raise InvalidArchetypeError(
                    f"Invalid archetype: {self.archetype}. "
                    f"Must be one of {[a.value for a in Archetype]}"
                )
        
        # Validate genres
        if not self.genres:
            raise InvalidAlbumError("Album must have at least one genre")
        
        validated_genres = []
        for genre in self.genres:
            if not isinstance(genre, Genre):
                try:
                    validated_genres.append(Genre(genre))
                except ValueError:
                    raise InvalidGenreError(
                        f"Invalid genre: {genre}. "
                        f"Must be one of {[g.value for g in Genre]}"
                    )
            else:
                validated_genres.append(genre)
        self.genres = validated_genres
        
        # Validate tracks
        if not isinstance(self.tracks, list):
            raise InvalidAlbumError("Tracks must be a list")
    
    def add_track(self, track: Track) -> None:
        """Add a track to the album."""
        if not isinstance(track, Track):
            from src.domain.exceptions.domain_errors import InvalidTrackError
            raise InvalidTrackError("Must provide a valid Track object")
        
        self.tracks.append(track)
    
    def get_track_count(self) -> int:
        """Get the number of tracks in the album."""
        return len(self.tracks)
    
    def get_total_duration(self) -> Optional[int]:
        """Get total album duration in seconds."""
        if all(t.duration_estimate is not None for t in self.tracks):
            return sum(t.duration_estimate for t in self.tracks)
        return None
    
    def __str__(self) -> str:
        """String representation."""
        return f"Album('{self.title}', {self.archetype.value}, {len(self.tracks)} tracks)"
