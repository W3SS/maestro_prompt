"""
Port (Interface) for LLM Client.

This is the OUTPUT PORT that the application requires.
Any LLM provider (Ollama, OpenAI, Claude) must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Optional


class ILLMClient(ABC):
    """Interface for LLM clients."""
    
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text from LLM.
        
        Args:
            prompt: User prompt
            system: System message (optional)
            temperature: Sampling temperature
            **kwargs: Provider-specific parameters
            
        Returns:
            Generated text
            
        Raises:
            Exception: Provider-specific errors
        """
        pass
        
    @abstractmethod
    async def close(self):
        """Close any open connections."""
        pass
