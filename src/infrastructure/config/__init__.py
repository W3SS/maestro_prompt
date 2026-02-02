"""Configuration management with multi-LLM provider support."""

from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

LLMProvider = Literal["gemini", "ollama", "lmstudio"]

class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    LLM Provider Options:
    - gemini: Google Gemini API (default)
    - ollama: Ollama Docker/Local instance
    - lmstudio: LM Studio Server
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="MAESTRO_",
        extra="ignore"
    )
    
    # === LLM Provider Configuration ===
    llm_provider: LLMProvider = Field(
        default="gemini",
        description="LLM provider to use (gemini|ollama|lmstudio)"
    )
    
    # Gemini
    gemini_api_key: Optional[str] = Field(default=None, description="Google Gemini API key")
    gemini_model: str = Field(default="gemini-1.5-flash", description="Gemini model name")
    
    # Ollama
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL (Docker or local)"
    )
    ollama_model: str = Field(default="llama3", description="Ollama model name")
    
    # LM Studio
    lmstudio_base_url: str = Field(
        default="http://localhost:1234/v1",
        description="LM Studio server URL"
    )
    lmstudio_model: str = Field(default="local-model", description="LM Studio model name")
    
    # Legacy/Backwards compatibility
    llm_base_url: str = Field(
        default="http://localhost:11434",
        description="[Legacy] Base URL for LLM"
    )
    llm_model: str = Field(
        default="mistral-nemo:12b",
        description="[Legacy] LLM model name"
    )
    llm_timeout: int = Field(default=1300, ge=1, description="LLM timeout in seconds")
    llm_max_retries: int = Field(default=3, ge=0, description="Max retries for LLM")
    
    # === Application Settings ===
    app_name: str = Field(default="Maestro AI", description="Application name")
    app_version: str = Field(default="0.2.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # === Data Paths ===
    data_dir: str = Field(default="data", description="Data directory for batches")
    context_dir: str = Field(default="contexts", description="Context JSON files directory")
    context_data_dir: str = Field(default="./data", description="[Legacy] Context data directory")
    output_dir: str = Field(default="./output", description="Output directory")
    
    # === API Configuration ===
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, ge=1, le=65535, description="API port")

    # === Database Configuration ===
    database_url: str = Field(
        default="sqlite+aiosqlite:///./maestro.db",
        description="Database URL (Async)"
    )
    persistence_type: str = Field(
        default="sqlalchemy", # Default to SQL for Phase 4
        description="Persistence type: 'json' or 'sqlalchemy'"
    )

# Singleton instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get or create settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

def reset_settings() -> None:
    """Reset settings (useful for testing)."""
    global _settings
    _settings = None
