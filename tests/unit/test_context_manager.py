"""
🔴 RED PHASE: Tests for Context Manager Module
-----------------------------------------------
Tests will FAIL until we implement src/context_manager.py

Test Coverage:
- Archetype-specific JSON loading (only load relevant data)
- Caching mechanism (avoid re-loading same data)
- Payload size reduction (verify 60% reduction target)
- Error handling (missing files, invalid JSON)
"""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import json
from src.context_manager import ContextManager, ContextConfig, ContextError


class TestContextConfig:
    """Test context configuration."""
    
    def test_default_config(self):
        """Should create config with defaults."""
        config = ContextConfig()
        
        assert config.data_dir == Path("data")
        assert config.cache_enabled is True
        assert config.cache_ttl == 3600  # 1 hour
        
    def test_custom_data_directory(self):
        """Should allow custom data directory."""
        config = ContextConfig(data_dir=Path("/custom/data"))
        
        assert config.data_dir == Path("/custom/data")
        
    def test_disable_cache(self):
        """Should allow disabling cache."""
        config = ContextConfig(cache_enabled=False)
        
        assert config.cache_enabled is False


class TestContextManager:
    """Test context manager with smart loading."""
    
    def test_initialization(self, data_dir):
        """Should initialize with data directory."""
        manager = ContextManager(ContextConfig(data_dir=data_dir))
        
        assert manager.config.data_dir == data_dir
        assert manager._cache == {}
        
    def test_load_archetype_specific_data(self, data_dir, mock_archetype_data):
        """Should load only archetype-specific data."""
        # Mock file reading
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_archetype_data))):
            manager = ContextManager(ContextConfig(data_dir=data_dir))
            
            # Load only cosmic_horror archetype
            context = manager.get_archetype_context("cosmic_horror")
            
            assert "cosmic_horror" in context
            assert context["cosmic_horror"]["name"] == "Cosmic Horror"
            # Should not load other archetypes
            assert len(context) == 1
            
    def test_cache_hit_avoids_reload(self, data_dir, mock_archetype_data):
        """Should use cached data on second call."""
        file_content = json.dumps(mock_archetype_data)
        
        with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
            manager = ContextManager(ContextConfig(data_dir=data_dir, cache_enabled=True))
            
            # First call - should read file
            context1 = manager.get_archetype_context("cosmic_horror")
            first_call_count = mock_file.call_count
            
            # Second call - should use cache
            context2 = manager.get_archetype_context("cosmic_horror")
            second_call_count = mock_file.call_count
            
            # File should not be read again
            assert first_call_count == second_call_count
            assert context1 == context2
            
    def test_cache_disabled_always_reloads(self, data_dir, mock_archetype_data):
        """Should reload data when cache is disabled."""
        file_content = json.dumps(mock_archetype_data)
        
        with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
            manager = ContextManager(ContextConfig(data_dir=data_dir, cache_enabled=False))
            
            # First call
            _ = manager.get_archetype_context("cosmic_horror")
            first_count = mock_file.call_count
            
            # Second call
            _ = manager.get_archetype_context("cosmic_horror")
            second_count = mock_file.call_count
            
            # File should be read twice
            assert second_count > first_count
            
    def test_payload_size_reduction(self, data_dir):
        """Should reduce payload size by loading only relevant data."""
        # Full archetypes file (simulated)
        full_data = {
            f"archetype_{i}": {"name": f"Archetype {i}", "data": "x" * 1000}
            for i in range(100)  # 100 archetypes
        }
        
        # Add target archetype
        full_data["cosmic_horror"] = {
            "name": "Cosmic Horror",
            "data": "specific_data"
        }
        
        with patch("builtins.open", mock_open(read_data=json.dumps(full_data))):
            with patch("pathlib.Path.exists", return_value=True):
                manager = ContextManager(ContextConfig(data_dir=data_dir))
                
                # Load only one archetype
                context = manager.get_archetype_context("cosmic_horror")
                
                # Should have only 1 archetype vs 100
                full_size = len(json.dumps(full_data))
                reduced_size = len(json.dumps(context))
                
                reduction_percent = (1 - reduced_size / full_size) * 100
                
                # Should reduce by at least 60%
                assert reduction_percent >= 60
                
    def test_missing_data_file_raises_error(self, data_dir):
        """Should raise ContextError if data file missing."""
        with patch("pathlib.Path.exists", return_value=False):
            manager = ContextManager(ContextConfig(data_dir=data_dir))
            
            with pytest.raises(ContextError) as exc_info:
                manager.get_archetype_context("missing_archetype")
                
            assert "not found" in str(exc_info.value).lower()
            
    def test_invalid_json_raises_error(self, data_dir):
        """Should raise ContextError on invalid JSON."""
        with patch("builtins.open", mock_open(read_data="invalid json {")):
            with patch("pathlib.Path.exists", return_value=True):
                manager = ContextManager(ContextConfig(data_dir=data_dir))
                
                with pytest.raises(ContextError) as exc_info:
                    manager.get_archetype_context("cosmic_horror")
                    
                assert "parse" in str(exc_info.value).lower() or "json" in str(exc_info.value).lower()
                
    def test_get_genre_fusion_context(self, data_dir, mock_genre_fusion):
        """Should load genre fusion data for specific genres."""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_genre_fusion))):
            with patch("pathlib.Path.exists", return_value=True):
                manager = ContextManager(ContextConfig(data_dir=data_dir))
                
                context = manager.get_genre_fusion_context("Dark Ambient", "Post-Metal")
                
                assert "Dark Ambient + Post-Metal" in context
                assert context["Dark Ambient + Post-Metal"]["result_style"] == "Atmospheric Doom"
                
    def test_cache_clear(self, data_dir, mock_archetype_data):
        """Should clear cache on demand."""
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_archetype_data))):
            with patch("pathlib.Path.exists", return_value=True):
                manager = ContextManager(ContextConfig(data_dir=data_dir))
                
                # Load data
                _ = manager.get_archetype_context("cosmic_horror")
                assert len(manager._cache) > 0
                
                # Clear cache
                manager.clear_cache()
                assert len(manager._cache) == 0
                
    def test_get_full_context_for_album_design(self, data_dir, mock_archetype_data, mock_genre_fusion):
        """Should build complete context for album design."""
        # This is the main use case - get all relevant data for a specific album
        archetype_data = json.dumps(mock_archetype_data)
        genre_data = json.dumps(mock_genre_fusion)
        
        def mock_open_multi(filename, *args, **kwargs):
            if "aesthetics" in str(filename):
                return mock_open(read_data=archetype_data)()
            elif "genre_fusion" in str(filename):
                return mock_open(read_data=genre_data)()
            return mock_open(read_data="{}")()
            
        with patch("builtins.open", mock_open_multi):
            with patch("pathlib.Path.exists", return_value=True):
                manager = ContextManager(ContextConfig(data_dir=data_dir))
                
                # Get full context for cosmic horror album with dark ambient
                context = manager.get_full_context(
                    archetype="cosmic_horror",
                    genres=["Dark Ambient", "Post-Metal"]
                )
                
                # Should contain archetype data
                assert "archetype" in context
                assert context["archetype"]["name"] == "Cosmic Horror"
                
                # Should contain genre fusion data
                assert "genre_fusion" in context


class TestContextError:
    """Test custom exception."""
    
    def test_context_error(self):
        """Should create context error."""
        error = ContextError("Data file not found")
        assert isinstance(error, Exception)
        assert "not found" in str(error).lower()
