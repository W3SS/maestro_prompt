"""
Ollama Adapter - Implementation of ILLMClient Port
---------------------------------------------------
Async Ollama client with timeout, retry, and connection pooling.

This adapter implements the ILLMClient port interface,
following Hexagonal Architecture principles.

Features:
- Configurable timeout (1300s for 12b models)
- Exponential backoff (3 retries, 2^n delay)
- Connection pooling via httpx.AsyncClient
- Proper error handling with custom exceptions
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import httpx

from src.ports.output.llm_client_port import ILLMClient


# Custom Exceptions
class LLMError(Exception):
    """Base exception for LLM client errors."""
    pass


class TimeoutError(LLMError):
    """Raised when LLM request times out."""
    pass


class RetryError(LLMError):
    """Raised when max retries are exceeded."""
    pass


@dataclass
class LLMConfig:
    """Configuration for LLM client."""
    
    base_url: str = "http://localhost:11434"
    model: str = "mistral-nemo:12b"
    timeout: int = 1300  # seconds (default for 12b models)
    max_retries: int = 3
    base_delay: int = 1  # seconds for exponential backoff
    headers: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate configuration."""
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative")


class LLMClient(ILLMClient):
    """
    Ollama LLM Client Adapter (implements ILLMClient port).
    
    Usage:
        async with LLMClient() as client:
            response = await client.generate("Design an album")
            
    Or:
        client = LLMClient()
        response = await client.generate("Design an album")
        await client.close()
    """
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize LLM client.
        
        Args:
            config: LLM configuration (uses defaults if None)
        """
        self.config = config or LLMConfig()
        self._client: Optional[httpx.AsyncClient] = None
        
    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create httpx client (connection pooling)."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.config.base_url,
                timeout=httpx.Timeout(self.config.timeout),
            )
        return self._client
        
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text from LLM with retry logic.
        
        Args:
            prompt: User prompt
            system: System message (optional)
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional Ollama API parameters
            
        Returns:
            Generated text
            
        Raises:
            TimeoutError: Request timed out
            RetryError: Max retries exceeded
            LLMError: Other LLM errors
        """
        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                **kwargs.get("options", {})
            }
        }
        
        if system:
            payload["system"] = system
            
        # Merge custom headers
        headers = {**self.config.headers}
        
        for attempt in range(self.config.max_retries + 1):
            try:
                response = await self.client.post(
                    "/api/generate",
                    json=payload,
                    headers=headers,
                    timeout=self.config.timeout
                )
                
                # Handle rate limiting
                if response.status_code == 429:
                    if attempt < self.config.max_retries:
                        delay = self.config.base_delay * (2 ** attempt)
                        await asyncio.sleep(delay)
                        continue
                    raise LLMError("Rate limit exceeded")
                    
                response.raise_for_status()
                data = response.json()
                
                return data.get("response", "")
                
            except httpx.TimeoutException as e:
                if attempt == self.config.max_retries:
                    raise TimeoutError(
                        f"Request timeout after {self.config.timeout}s"
                    ) from e
                    
                # Exponential backoff for retries
                delay = self.config.base_delay * (2 ** attempt)
                time.sleep(delay)  # Synchronous sleep for backoff
                
            except httpx.NetworkError as e:
                if attempt == self.config.max_retries:
                    raise RetryError(
                        f"Network error after {self.config.max_retries} retries: {e}"
                    ) from e
                    
                # Exponential backoff
                delay = self.config.base_delay * (2 ** attempt)
                time.sleep(delay)
                
            except httpx.HTTPStatusError as e:
                raise LLMError(f"HTTP error: {e.response.status_code}") from e
                
        # Should never reach here, but just in case
        raise RetryError(f"Failed after {self.config.max_retries} retries")
        
    async def close(self):
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            
    async def __aenter__(self):
        """Context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()
        return False
