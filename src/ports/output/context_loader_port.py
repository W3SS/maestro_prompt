"""
Port (Interface) for Context Loader.

This is the OUTPUT PORT for loading JSON context data.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IContextLoader(ABC):
    """Interface for context loading."""
    
    @abstractmethod
    def get_archetype_context(self, archetype: str) -> Dict[str, Any]:
        """Load context for specific archetype."""
        pass
        
    @abstractmethod
    def get_genre_fusion_context(self, genre1: str, genre2: str) -> Dict[str, Any]:
        """Load genre fusion data."""
        pass
        
    @abstractmethod
    def get_full_context(self, archetype: str, genres: List[str]) -> Dict[str, Any]:
        """Build complete context for album design."""
        pass
        
    @abstractmethod
    def clear_cache(self):
        """Clear cached data."""
        pass
