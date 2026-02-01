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
        case_sensitive=False
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
    
    # === Application Settings ===
    app_name: str = Field(default="Maestro AI", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    
    # === Data Paths ===
    data_dir: str = Field(default="data", description="Data directory for batches")
    context_dir: str = Field(default="contexts", description="Context JSON files directory")

# Singleton instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get or create settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
