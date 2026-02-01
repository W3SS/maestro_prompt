"""Unit tests for Album and Track domain models."""

import pytest
from datetime import datetime

from src.domain.models.album import Album, Track, Archetype, Genre
from src.domain.exceptions.domain_errors import (
    InvalidAlbumError,
    InvalidTrackError,
    InvalidArchetypeError,
    InvalidGenreError
)


class TestTrack:
    """Test Track entity."""
    
    def test_track_creation_valid(self):
        """Should create a valid track."""
        track = Track(
            title="Cosmic Dread",
            lyrics="In the void between stars...",
            style_tags=["heavy metal", "atmospheric"],
            track_number=1
        )
        
        assert track.title == "Cosmic Dread"
        assert "void" in track.lyrics
        assert track.track_number == 1
        assert track.duration_estimate is None
    
    def test_track_with_duration(self):
        """Should create track with duration."""
        track = Track(
            title="Test",
            lyrics="Test lyrics",
            style_tags=["test"],
            duration_estimate=180
        )
        
        assert track.duration_estimate == 180
    
    def test_track_empty_title_raises_error(self):
        """Should raise error for empty title."""
        with pytest.raises(InvalidTrackError, match="title cannot be empty"):
            Track(
                title="",
                lyrics="Lyrics",
                style_tags=["tag"]
            )
    
    def test_track_whitespace_title_raises_error(self):
        """Should raise error for whitespace-only title."""
        with pytest.raises(InvalidTrackError, match="title cannot be empty"):
            Track(
                title="   ",
                lyrics="Lyrics",
                style_tags=["tag"]
            )
    
    def test_track_empty_lyrics_raises_error(self):
        """Should raise error for empty lyrics."""
        with pytest.raises(InvalidTrackError, match="lyrics cannot be empty"):
            Track(
                title="Title",
                lyrics="",
                style_tags=["tag"]
            )
    
    def test_track_invalid_track_number_raises_error(self):
        """Should raise error for track number < 1."""
        with pytest.raises(InvalidTrackError, match="Track number must be >= 1"):
            Track(
                title="Title",
                lyrics="Lyrics",
                style_tags=["tag"],
                track_number=0
            )
    
    def test_track_negative_duration_raises_error(self):
        """Should raise error for negative duration."""
        with pytest.raises(InvalidTrackError, match="Duration must be positive"):
            Track(
                title="Title",
                lyrics="Lyrics",
                style_tags=["tag"],
                duration_estimate=-10
            )


class TestAlbum:
    """Test Album entity."""
    
    def test_album_creation_valid(self):
        """Should create a valid album."""
        album = Album(
            title="Echoes of the Void",
            archetype=Archetype.COSMIC_HORROR,
            genres=[Genre.METAL, Genre.JAZZ]
        )
        
        assert album.title == "Echoes of the Void"
        assert album.archetype == Archetype.COSMIC_HORROR
        assert len(album.genres) == 2
        assert album.get_track_count() == 0
        assert isinstance(album.created_at, datetime)
    
    def test_album_with_string_archetype(self):
        """Should convert string archetype to Enum."""
        album = Album(
            title="Test Album",
            archetype="cosmic_horror",  # String instead of Enum
            genres=[Genre.METAL]
        )
        
        assert album.archetype == Archetype.COSMIC_HORROR
    
    def test_album_with_string_genres(self):
        """Should convert string genres to Enum."""
        album = Album(
            title="Test Album",
            archetype=Archetype.DYSTOPIAN_REBELLION,
            genres=["metal", "jazz"]  # Strings instead of Enums
        )
        
        assert album.genres[0] == Genre.METAL
        assert album.genres[1] == Genre.JAZZ
    
    def test_album_empty_title_raises_error(self):
        """Should raise error for empty title."""
        with pytest.raises(InvalidAlbumError, match="title cannot be empty"):
            Album(
                title="",
                archetype=Archetype.COSMIC_HORROR,
                genres=[Genre.METAL]
            )
    
    def test_album_invalid_archetype_raises_error(self):
        """Should raise error for invalid archetype."""
        with pytest.raises(InvalidArchetypeError, match="Invalid archetype"):
            Album(
                title="Test",
                archetype="invalid_archetype",
                genres=[Genre.METAL]
            )
    
    def test_album_no_genres_raises_error(self):
        """Should raise error for empty genres list."""
        with pytest.raises(InvalidAlbumError, match="at least one genre"):
            Album(
                title="Test",
                archetype=Archetype.COSMIC_HORROR,
                genres=[]
            )
    
    def test_album_invalid_genre_raises_error(self):
        """Should raise error for invalid genre."""
        with pytest.raises(InvalidGenreError, match="Invalid genre"):
            Album(
                title="Test",
                archetype=Archetype.COSMIC_HORROR,
                genres=["invalid_genre"]
            )
    
    def test_album_add_track(self):
        """Should add track to album."""
        album = Album(
            title="Test",
            archetype=Archetype.COSMIC_HORROR,
            genres=[Genre.METAL]
        )
        
        track = Track(
            title="Track 1",
            lyrics="Lyrics",
            style_tags=["tag"]
        )
        
        album.add_track(track)
        
        assert album.get_track_count() == 1
        assert album.tracks[0] == track
    
    def test_album_add_invalid_track_raises_error(self):
        """Should raise error when adding non-Track object."""
        album = Album(
            title="Test",
            archetype=Archetype.COSMIC_HORROR,
            genres=[Genre.METAL]
        )
        
        with pytest.raises(InvalidTrackError, match="valid Track object"):
            album.add_track("not a track")
    
    def test_album_get_total_duration_with_all_durations(self):
        """Should calculate total duration when all tracks have durations."""
        album = Album(
            title="Test",
            archetype=Archetype.COSMIC_HORROR,
            genres=[Genre.METAL]
        )
        
        album.add_track(Track(
            title="Track 1",
            lyrics="Lyrics",
            style_tags=["tag"],
            duration_estimate=180
        ))
        album.add_track(Track(
            title="Track 2",
            lyrics="Lyrics",
            style_tags=["tag"],
            duration_estimate=200
        ))
        
        assert album.get_total_duration() == 380
    
    def test_album_get_total_duration_with_missing_durations(self):
        """Should return None when some tracks lack durations."""
        album = Album(
            title="Test",
            archetype=Archetype.COSMIC_HORROR,
            genres=[Genre.METAL]
        )
        
        album.add_track(Track(
            title="Track 1",
            lyrics="Lyrics",
            style_tags=["tag"],
            duration_estimate=180
        ))
        album.add_track(Track(
            title="Track 2",
            lyrics="Lyrics",
            style_tags=["tag"]
            # No duration
        ))
        
        assert album.get_total_duration() is None
    
    def test_album_string_representation(self):
        """Should have meaningful string representation."""
        album = Album(
            title="Test Album",
            archetype=Archetype.COSMIC_HORROR,
            genres=[Genre.METAL]
        )
        
        album_str = str(album)
        
        assert "Test Album" in album_str
        assert "cosmic_horror" in album_str
        assert "0 tracks" in album_str


class TestArchetype:
    """Test Archetype enum."""
    
    def test_archetype_values(self):
        """Should have expected archetype values."""
        assert Archetype.COSMIC_HORROR.value == "cosmic_horror"
        assert Archetype.DYSTOPIAN_REBELLION.value == "dystopian_rebellion"
        assert Archetype.COLLEGE_COMING_OF_AGE.value == "college_coming_of_age"
    
    def test_archetype_from_string(self):
        """Should create archetype from string."""
        archetype = Archetype("cosmic_horror")
        assert archetype == Archetype.COSMIC_HORROR


class TestGenre:
    """Test Genre enum."""
    
    def test_genre_values(self):
        """Should have expected genre values."""
        assert Genre.METAL.value == "metal"
        assert Genre.JAZZ.value == "jazz"
        assert Genre.PROGRESSIVE_ROCK.value == "progressive_rock"
    
    def test_genre_from_string(self):
        """Should create genre from string."""
        genre = Genre("metal")
        assert genre == Genre.METAL
