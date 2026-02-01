"""
Pytest fixtures for Maestro AI tests.

This module provides reusable fixtures for:
- Mock Ollama HTTP responses
- JSON data loading
- Temporary file management
- Async test utilities
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def data_dir() -> Path:
    """Return path to data directory."""
    return Path(__file__).parent.parent / "data"


@pytest.fixture
def mock_ollama_response() -> Dict[str, Any]:
    """Mock Ollama API response for generation."""
    return {
        "model": "mistral-nemo:12b",
        "created_at": "2026-02-01T10:00:00Z",
        "response": "Test generated content",
        "done": True,
        "context": [1, 2, 3],
        "total_duration": 5000000000,
        "load_duration": 1000000000,
        "prompt_eval_count": 50,
        "prompt_eval_duration": 2000000000,
        "eval_count": 100,
        "eval_duration": 2000000000,
    }


@pytest.fixture
def mock_archetype_data() -> Dict[str, Any]:
    """Mock archetype data for cosmic_horror."""
    return {
        "cosmic_horror": {
            "name": "Cosmic Horror",
            "theme": "Unknown entities beyond comprehension",
            "visual_palette": ["Black", "Deep Purple", "Starfield"],
            "sonic_signature": "Dark Ambient, Drone Metal",
            "narrative_arc": "Discovery → Obsession → Madness → Revelation",
            "key_symbols": ["Eyes", "Stars", "Void", "Ancient Texts"],
            "emotional_journey": ["Curiosity", "Dread", "Awe", "Nihilism"],
        }
    }


@pytest.fixture
def mock_genre_fusion() -> Dict[str, Any]:
    """Mock genre fusion matrix entry."""
    return {
        "Dark Ambient + Post-Metal": {
            "primary_genre": "Dark Ambient",
            "fusion_genre": "Post-Metal",
            "result_style": "Atmospheric Doom",
            "instruments": ["Modular Synth", "Baritone Guitar", "Field Recordings"],
            "tempo_range": "40-60 BPM",
            "production_notes": "Heavy reverb, minimal drums, drone layers",
        }
    }


@pytest.fixture
def mock_httpx_client():
    """Mock httpx.AsyncClient for Ollama API calls."""
    mock_client = AsyncMock()
    mock_response = MagicMock()  # Use MagicMock for response, not AsyncMock
    mock_response.status_code = 200
    mock_response.json.return_value = {  # json() is synchronous
        "response": "Generated album design",
        "done": True,
    }
    mock_response.raise_for_status = MagicMock()  # Synchronous method
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.aclose = AsyncMock()
    return mock_client



@pytest.fixture
def temp_checkpoint_file(tmp_path):
    """Create temporary checkpoint file for testing."""
    checkpoint_path = tmp_path / ".maestro_state.json"
    
    # Pre-populate with sample state
    state = {
        "album": "Test Album",
        "tracks_completed": 2,
        "tracks_total": 8,
        "last_track": "Track 2",
        "timestamp": "2026-02-01T10:00:00Z",
    }
    
    checkpoint_path.write_text(json.dumps(state, indent=2))
    return checkpoint_path


@pytest.fixture
def sample_album_data() -> Dict[str, Any]:
    """Sample album design data."""
    return {
        "album_title": "Echoes from the Abyss",
        "archetype": "cosmic_horror",
        "narrative": "An astronomer's descent into madness",
        "tracks": [
            {
                "title": "Stellar Whispers",
                "theme": "First signals from unknown",
                "genre": "Dark Ambient",
                "mood": "Anticipation",
            },
            {
                "title": "The Void Speaks",
                "theme": "Decoding the message",
                "genre": "Drone Metal",
                "mood": "Dread",
            },
        ],
    }


@pytest.fixture
def sample_suno_track() -> Dict[str, Any]:
    """Sample Suno batch track entry."""
    return {
        "id": 1,
        "album": "Echoes from the Abyss",
        "title": "Stellar Whispers",
        "style_prompt": "[Is_MAX_MODE: MAX](MAX)\nDark Ambient, Drone Synth, Lo-Fi Drum Machine",
        "lyrics": "[Intro]\nIn the silent hum of cosmic winds...\n\n[Verse 1]\nStars align in patterns strange...",
    }


@pytest.fixture(autouse=True)
def reset_cache():
    """Reset any global caches between tests."""
    # This will be implemented when we add caching to context_manager
    yield
    # Cleanup after test


@pytest.fixture
def mock_time():
    """Mock time module for testing retry delays."""
    with patch("time.sleep") as mock_sleep:
        yield mock_sleep
