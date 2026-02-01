"""Ollama LLM Client Adapter."""

import httpx
from typing import Optional
from src.ports.output.llm_client_port import ILLMClient

class OllamaClient(ILLMClient):
    """
    Ollama LLM client adapter.
    
    Supports Ollama running in Docker or locally.
    Default URL: http://localhost:11434
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama server URL
            model: Model name (e.g., 'llama3', 'mistral', 'codellama')
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: User prompt
            system: System message (optional)
            temperature: Sampling temperature
            **kwargs: Additional Ollama parameters (stream, top_p, etc.)
        
        Returns:
            Generated text
        
        Raises:
            httpx.HTTPError: Connection or API errors
        """
        endpoint = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system or "",
            "temperature": temperature,
            "stream": False,
            **kwargs
        }
        
        try:
            response = await self.client.post(endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        
        except httpx.HTTPError as e:
            raise Exception(f"Ollama API error: {e}")
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
