"""
🔴 RED PHASE: Tests for LLM Client Module
------------------------------------------
Tests will FAIL until we implement src/llm_client.py

Test Coverage:
- Timeout configuration (configurable per model)
- Exponential backoff (3 retries with 2^n delay)
- Connection pooling (httpx AsyncClient reuse)
- Error handling (network, timeout, rate limit)
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from src.llm_client import LLMClient, LLMConfig, LLMError, TimeoutError, RetryError


class TestLLMConfig:
    """Test LLM configuration dataclass."""
    
    def test_default_config(self):
        """Should create config with sensible defaults."""
        config = LLMConfig()
        
        assert config.base_url == "http://localhost:11434"
        assert config.model == "mistral-nemo:12b"
        assert config.timeout == 1300  # 12b model default
        assert config.max_retries == 3
        assert config.base_delay == 1
        
    def test_custom_timeout_for_8b_model(self):
        """Should allow shorter timeout for smaller models."""
        config = LLMConfig(model="llama3:8b", timeout=300)
        
        assert config.timeout == 300
        assert config.model == "llama3:8b"
        
    def test_retry_config(self):
        """Should configure retry behavior."""
        config = LLMConfig(max_retries=5, base_delay=2)
        
        assert config.max_retries == 5
        assert config.base_delay == 2


class TestLLMClient:
    """Test LLM client with async operations."""
    
    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Should initialize with correct config and lazy client."""
        client = LLMClient()
        
        assert client.config.model == "mistral-nemo:12b"
        # Client is lazy-loaded, should be None until first use  
        assert client._client is None
        # Accessing client property should create it
        _ = client.client
        assert client._client is not None
        
    @pytest.mark.asyncio
    async def test_successful_generation(self, mock_httpx_client):
        """Should generate text successfully."""
        with patch("httpx.AsyncClient", return_value=mock_httpx_client):
            client = LLMClient()
            
            result = await client.generate(
                prompt="Design an album",
                system="You are a music AI"
            )
            
            assert "Generated album design" in result
            mock_httpx_client.post.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_timeout_configuration(self):
        """Should use configured timeout in HTTP request."""
        mock_client = AsyncMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Test", "done": True}
        mock_response.raise_for_status = MagicMock()
        
        mock_client.post = AsyncMock(return_value=mock_response)
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            client = LLMClient(LLMConfig(timeout=1300))
            
            await client.generate("test prompt")
            
            # Verify timeout was passed to httpx  
            call_kwargs = mock_client.post.call_args.kwargs
            assert call_kwargs["timeout"] == 1300

            
    @pytest.mark.asyncio
    async def test_exponential_backoff_on_network_error(self, mock_time):
        """Should retry with exponential backoff on network errors."""
        mock_client = AsyncMock()
        
        # Create success response
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"response": "Success", "done": True}
        success_response.raise_for_status = MagicMock()
        
        # Mock post to fail twice then succeed
        mock_client.post = AsyncMock(side_effect=[
            httpx.NetworkError("Connection failed"),
            httpx.NetworkError("Connection failed"),
            success_response
        ])
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            client = LLMClient(LLMConfig(max_retries=3, base_delay=1))
            
            result = await client.generate("test")
            
            assert result == "Success"
            assert mock_client.post.call_count == 3
            
            # Verify exponential delays: 1s, 2s
            assert mock_time.call_count == 2
            assert mock_time.call_args_list[0][0][0] == 1  # 2^0
            assert mock_time.call_args_list[1][0][0] == 2  # 2^1
            
    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self):
        """Should raise RetryError after max retries."""
        mock_client = AsyncMock()
        mock_client.post.side_effect = httpx.NetworkError("Persistent error")
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            client = LLMClient(LLMConfig(max_retries=2))
            
            with pytest.raises(RetryError) as exc_info:
                await client.generate("test")
                
            assert "2 retries" in str(exc_info.value).lower()
            assert mock_client.post.call_count == 3  # initial + 2 retries
            
    @pytest.mark.asyncio
    async def test_timeout_error_handling(self):
        """Should raise TimeoutError on request timeout."""
        mock_client = AsyncMock()
        mock_client.post.side_effect = httpx.TimeoutException("Request timeout")
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            client = LLMClient()
            
            with pytest.raises(TimeoutError) as exc_info:
                await client.generate("long prompt")
                
            # Use .lower() for case-insensitive check
            assert "timeout" in str(exc_info.value).lower()
            
    @pytest.mark.asyncio
    async def test_rate_limit_handling(self):
        """Should handle 429 rate limit with backoff."""
        mock_client = AsyncMock()
        
        # Rate limit response
        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 429
        
        # Success response
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = {"response": "Success after rate limit", "done": True}
        success_response.raise_for_status = MagicMock()
        
        mock_client.post = AsyncMock(side_effect=[rate_limit_response, success_response])
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            client = LLMClient()
            
            result = await client.generate("test")
            
            assert "Success after rate limit" in result
            assert mock_client.post.call_count == 2
            
    @pytest.mark.asyncio
    async def test_connection_reuse(self):
        """Should reuse httpx client for multiple requests."""
        mock_client = AsyncMock()
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Test", "done": True}
        mock_response.raise_for_status = MagicMock()
        
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.aclose = AsyncMock()
        
        with patch("httpx.AsyncClient", return_value=mock_client) as client_factory:
            client = LLMClient()
            
            await client.generate("test 1")
            await client.generate("test 2")
            await client.generate("test 3")
            
            # Client should be created only once
            assert client_factory.call_count == 1
            # But used multiple times
            assert mock_client.post.call_count == 3
            
    @pytest.mark.asyncio
    async def test_context_manager_cleanup(self):
        """Should properly close client on context exit."""
        mock_client = AsyncMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Test", "done": True}
        mock_response.raise_for_status = MagicMock()
        
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.aclose = AsyncMock()
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            async with LLMClient() as client:
                await client.generate("test")
                
            # Verify aclose was called
            mock_client.aclose.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_streaming_response(self):
        """Should support streaming for long generations."""
        # This test will be implemented when we add streaming support
        pytest.skip("Streaming feature not yet in scope")
        
    @pytest.mark.asyncio
    async def test_custom_headers(self):
        """Should allow custom headers (e.g., auth tokens)."""
        mock_client = AsyncMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Test", "done": True}
        mock_response.raise_for_status = MagicMock()
        
        mock_client.post = AsyncMock(return_value=mock_response)
        
        with patch("httpx.AsyncClient", return_value=mock_client):
            config = LLMConfig(headers={"Authorization": "Bearer test-token"})
            client = LLMClient(config)
            
            await client.generate("test")
            
            call_kwargs = mock_client.post.call_args.kwargs
            assert call_kwargs["headers"]["Authorization"] == "Bearer test-token"


class TestLLMErrors:
    """Test custom exception hierarchy."""
    
    def test_llm_error_base(self):
        """Should create base LLM error."""
        error = LLMError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert isinstance(error, Exception)
        
    def test_timeout_error(self):
        """Should create timeout-specific error."""
        error = TimeoutError("Request took too long")
        assert isinstance(error, LLMError)
        assert "took too long" in str(error)
        
    def test_retry_error(self):
        """Should create retry-specific error."""
        error = RetryError("Max retries exceeded")
        assert isinstance(error, LLMError)
        # String is already lowercase in message, no need for .lower()
        assert "retries" in str(error).lower()  # Fixed to 'retries' (plural)
