"""Unit tests for DI Container."""

import pytest

from src.infrastructure.di.container import Container, get_container, reset_container
from src.ports.output.llm_client_port import ILLMClient
from src.ports.output.context_loader_port import IContextLoader
from src.application.services.album_designer import AlbumDesigner
from src.application.services.batch_manager import BatchManager


class TestContainer:
    """Test DI Container."""
    
    def teardown_method(self):
        """Reset container after each test."""
        reset_container()
    
    def test_container_provides_llm_client(self):
        """Should provide LLM client."""
        container = Container()
        
        llm_client = container.llm_client()
        
        assert llm_client is not None
        assert isinstance(llm_client, ILLMClient)
    
    def test_container_llm_client_is_singleton(self):
        """Should return same LLM client instance."""
        container = Container()
        
        client1 = container.llm_client()
        client2 = container.llm_client()
        
        assert client1 is client2
    
    def test_container_provides_context_loader(self):
        """Should provide context loader."""
        container = Container()
        
        context_loader = container.context_loader()
        
        assert context_loader is not None
        assert isinstance(context_loader, IContextLoader)
    
    def test_container_context_loader_is_singleton(self):
        """Should return same context loader instance."""
        container = Container()
        
        loader1 = container.context_loader()
        loader2 = container.context_loader()
        
        assert loader1 is loader2
    
    def test_container_provides_album_designer(self):
        """Should provide album designer service."""
        container = Container()
        
        designer = container.album_designer()
        
        assert designer is not None
        assert isinstance(designer, AlbumDesigner)
    
    def test_container_album_designer_is_singleton(self):
        """Should return same album designer instance."""
        container = Container()
        
        designer1 = container.album_designer()
        designer2 = container.album_designer()
        
        assert designer1 is designer2
    
    def test_container_provides_batch_manager(self):
        """Should provide batch manager service."""
        container = Container()
        
        manager = container.batch_manager()
        
        assert manager is not None
        assert isinstance(manager, BatchManager)
    
    def test_container_batch_manager_is_singleton(self):
        """Should return same batch manager instance."""
        container = Container()
        
        manager1 = container.batch_manager()
        manager2 = container.batch_manager()
        
        assert manager1 is manager2
    
    def test_container_reset(self):
        """Should reset all dependencies."""
        container = Container()
        
        client1 = container.llm_client()
        designer1 = container.album_designer()
        
        container.reset()
        
        client2 = container.llm_client()
        designer2 = container.album_designer()
        
        assert client1 is not client2
        assert designer1 is not designer2
    
    def test_get_container_singleton(self):
        """Should return same container instance."""
        container1 = get_container()
        container2 = get_container()
        
        assert container1 is container2
    
    def test_reset_container(self):
        """Should reset global container."""
        container1 = get_container()
        reset_container()
        container2 = get_container()
        
        assert container1 is not container2
    
    def test_album_designer_uses_injected_dependencies(self):
        """Should inject dependencies into album designer."""
        container = Container()
        
        designer = container.album_designer()
        
        # Verify it has the injected dependencies
        assert designer.llm is not None
        assert designer.context is not None
        assert designer.llm is container.llm_client()
        assert designer.context is container.context_loader()
