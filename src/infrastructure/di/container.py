"""Dependency Injection Container."""

from typing import Optional

from src.ports.output.llm_client_port import ILLMClient
from src.ports.output.context_loader_port import IContextLoader

# LLM Clients
from src.adapters.output.llm.ollama_adapter import LLMClient as GeminiClient, LLMConfig
from src.adapters.output.llm.ollama_client import OllamaClient
from src.adapters.output.llm.lmstudio_client import LMStudioClient

# Other adapters
from src.adapters.output.context.json_context_adapter import ContextManager, ContextConfig
from src.adapters.output.persistence.json_file_repository import JsonFileRepository

# Services
from src.application.services.album_designer import AlbumDesigner
from src.application.services.batch_manager import BatchManager

# Ports
from src.ports.output.batch_repository import IBatchRepository

# Config
from src.infrastructure.config import get_settings


class Container:
    """
    Dependency Injection Container.
    
    Manages creation and lifetime of application dependencies.
    Follows the Service Locator pattern.
    """
    
    def __init__(self):
        """Initialize container."""
        self._llm_client: Optional[ILLMClient] = None
        self._context_loader: Optional[IContextLoader] = None
        self._album_designer: Optional[AlbumDesigner] = None
        self._batch_manager: Optional[BatchManager] = None
    
    def llm_client(self) -> ILLMClient:
        """
        Get LLM client (singleton).
        
        Factory pattern: Returns appropriate client based on configuration.
        Supports: Gemini, Ollama, LM Studio.
        
        Returns:
            ILLMClient instance
        """
        if self._llm_client is None:
            settings = get_settings()
            
            # LLM Provider Factory
            if settings.llm_provider == "ollama":
                self._llm_client = OllamaClient(
                    base_url=settings.ollama_base_url,
                    model=settings.ollama_model
                )
            
            elif settings.llm_provider == "lmstudio":
                self._llm_client = LMStudioClient(
                    base_url=settings.lmstudio_base_url,
                    model=settings.lmstudio_model
                )
            
            else:  # Default to Gemini
                config = LLMConfig(
                    api_key=settings.gemini_api_key,
                    model=settings.gemini_model
                )
                self._llm_client = GeminiClient(config)
        
        return self._llm_client
    
    def context_loader(self) -> IContextLoader:
        """
        Get context loader (singleton).
        
        Returns:
            IContextLoader instance
        """
        if self._context_loader is None:
            settings = get_settings()
            config = ContextConfig(data_dir=settings.context_dir)
            self._context_loader = ContextManager(config)
        return self._context_loader
    
    def album_designer(self) -> AlbumDesigner:
        """
        Get album designer service (singleton).
        
        Returns:
            AlbumDesigner instance
        """
        if self._album_designer is None:
            self._album_designer = AlbumDesigner(
                llm_client=self.llm_client(),
                context_loader=self.context_loader()
            )
        return self._album_designer
    
    def batch_repository(self) -> IBatchRepository:
        """
        Get batch repository (singleton).
        
        Returns:
            IBatchRepository instance
        """
        # We could add a caching mechanism or singleton here if needed,
        # but JsonFileRepository is lightweight.
        # Singleton is better for concurrency if we had in-memory cache inside adapter.
        return JsonFileRepository()

    def batch_manager(self) -> BatchManager:
        """
        Get batch manager service (singleton).
        
        Returns:
            BatchManager instance
        """
        if self._batch_manager is None:
            self._batch_manager = BatchManager(
                repository=self.batch_repository()
            )
        return self._batch_manager
    
    def reset(self) -> None:
        """Reset all dependencies (useful for testing)."""
        self._llm_client = None
        self._context_loader = None
        self._album_designer = None
        self._batch_manager = None


# Global container instance
_container: Optional[Container] = None


def get_container() -> Container:
    """
    Get DI container (singleton pattern).
    
    Returns:
        Container instance
    """
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container() -> None:
    """Reset container (useful for testing)."""
    global _container
    if _container is not None:
        _container.reset()
    _container = None
