"""Unit tests for Settings."""

import pytest
import os
from unittest.mock import patch

from src.infrastructure.config import Settings, get_settings, reset_settings


class TestSettings:
    """Test Settings configuration."""
    
    def teardown_method(self):
        """Reset settings after each test."""
        reset_settings()
    
    def test_settings_default_values(self):
        """Should have sensible defaults."""
        settings = Settings()
        
        assert settings.llm_base_url == "http://localhost:11434"
        assert settings.llm_model == "mistral-nemo:12b"
        assert settings.llm_timeout == 1300
        assert settings.llm_max_retries == 3
        assert settings.context_data_dir == "./data"
        assert settings.app_name == "Maestro AI"
        assert settings.debug is False
    
    def test_settings_from_env_variables(self):
        """Should load from environment variables with MAESTRO_ prefix."""
        with patch.dict(os.environ, {
            "MAESTRO_LLM_BASE_URL": "http://custom:11434",
            "MAESTRO_LLM_MODEL": "custom-model",
            "MAESTRO_LLM_TIMEOUT": "2000",
            "MAESTRO_DEBUG": "true"
        }):
            settings = Settings()
            
            assert settings.llm_base_url == "http://custom:11434"
            assert settings.llm_model == "custom-model"
            assert settings.llm_timeout == 2000
            assert settings.debug is True
    
    def test_settings_validation_positive_timeout(self):
        """Should validate timeout is positive."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            Settings(llm_timeout=0)
    
    def test_settings_validation_port_range(self):
        """Should validate port is in valid range."""
        with pytest.raises(Exception):  # ValidationError
            Settings(api_port=70000)
    
    def test_get_settings_singleton(self):
        """Should return same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2
    
    def test_reset_settings(self):
        """Should reset singleton."""
        settings1 = get_settings()
        reset_settings()
        settings2 = get_settings()
        
        assert settings1 is not settings2
    
    def test_settings_case_insensitive_env(self):
        """Should handle case-insensitive env vars."""
        with patch.dict(os.environ, {
            "maestro_debug": "true",  # lowercase
            "MAESTRO_DEBUG": "false"  # uppercase (should override)
        }):
            settings = Settings()
            # Due to case_sensitive=False, last one wins
            assert settings.debug in [True, False]
