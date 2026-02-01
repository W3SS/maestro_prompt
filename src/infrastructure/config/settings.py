"""Application settings using Pydantic."""

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Environment variables are prefixed with MAESTRO_
    Example: MAESTRO_LLM_BASE_URL="http://localhost:11434"
    """
    
    # LLM Configuration
    llm_base_url: str = Field(
        default="http://localhost:11434",
        description="Base URL for Ollama LLM"
    )
    llm_model: str = Field(
        default="mistral-nemo:12b",
        description="LLM model name"
    )
    llm_timeout: int = Field(
        default=1300,
        ge=1,
        description="LLM request timeout in seconds"
    )
    llm_max_retries: int = Field(
        default=3,
        ge=0,
        description="Maximum number of retries for LLM requests"
    )
    
    # Context Configuration
    context_data_dir: str = Field(
        default="./data",
        description="Directory containing context data files"
    )
    
    # Application Configuration
    app_name: str = Field(
        default="Maestro AI",
        description="Application name"
    )
    app_version: str = Field(
        default="0.2.0",
        description="Application version"
    )
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    # Output Configuration
    output_dir: str = Field(
        default="./output",
        description="Directory for generated outputs"
    )
    
    # API Configuration (for future web API)
    api_host: str = Field(
        default="0.0.0.0",
        description="API host"
    )
    api_port: int = Field(
        default=8000,
        ge=1,
        le=65535,
        description="API port"
    )
    
    model_config = {
        "env_prefix": "MAESTRO_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get application settings (singleton pattern).
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset settings (useful for testing)."""
    global _settings
    _settings = None
