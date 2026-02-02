"""LM Studio LLM Client Adapter."""

import httpx
from typing import Optional
from src.ports.output.llm_client_port import ILLMClient

class LMStudioClient(ILLMClient):
    """
    LM Studio LLM client adapter.
    
    Supports LM Studio running locally with OpenAI-compatible API.
    Default URL: http://localhost:1234/v1
    """
    
    def __init__(self, base_url: str = "http://localhost:1234/v1", model: str = "local-model"):
        """
        Initialize LM Studio client.
        
        Args:
            base_url: LM Studio server URL (OpenAI-compatible endpoint)
            model: Model identifier (usually auto-detected by LM Studio)
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
        Generate text using LM Studio OpenAI-compatible API.
        
        Args:
            prompt: User prompt
            system: System message (optional)
            temperature: Sampling temperature
            **kwargs: Additional OpenAI parameters (max_tokens, top_p, etc.)
        
        Returns:
            Generated text
        
        Raises:
            httpx.HTTPError: Connection or API errors
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": kwargs.get("max_tokens", 2048),
            **{k: v for k, v in kwargs.items() if k != "max_tokens"}
        }
        
        try:
            response = await self.client.post(endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Extract content from OpenAI format
            return result["choices"][0]["message"]["content"]
        
        except httpx.HTTPError as e:
            raise Exception(f"LM Studio API error: {e}")
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
