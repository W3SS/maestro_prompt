"""Unit tests for Multi-LLM adapters (Ollama and LM Studio)."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.adapters.output.llm.ollama_client import OllamaClient
from src.adapters.output.llm.lmstudio_client import LMStudioClient


class TestOllamaClient:
    """Test suite for Ollama LLM adapter."""
    
    @pytest.mark.asyncio
    async def test_ollama_generate_success(self):
        """Should generate text using Ollama API."""
        client = OllamaClient(base_url="http://localhost:11434", model="llama3")
        
        # Mock httpx response
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Generated text from Ollama"}
        mock_response.raise_for_status = MagicMock()
        
        with patch.object(client.client, 'post', return_value=mock_response) as mock_post:
            result = await client.generate("Test prompt", temperature=0.8)
            
            assert result == "Generated text from Ollama"
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_ollama_with_system_message(self):
        """Should include system message in request."""
        client = OllamaClient()
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Response with system"}
        mock_response.raise_for_status = MagicMock()
        
        with patch.object(client.client, 'post', return_value=mock_response) as mock_post:
            await client.generate("Prompt", system="You are a helpful assistant")
            
            call_args = mock_post.call_args[1]['json']
            assert call_args['system'] == "You are a helpful assistant"


class TestLMStudioClient:
    """Test suite for LM Studio LLM adapter."""
    
    @pytest.mark.asyncio
    async def test_lmstudio_generate_success(self):
        """Should generate text using LM Studio OpenAI-compatible API."""
        client = LMStudioClient(base_url="http://localhost:1234/v1", model="local-model")
        
        # Mock OpenAI-style response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "Generated text from LM Studio"}}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch.object(client.client, 'post', return_value=mock_response) as mock_post:
            result = await client.generate("Test prompt")
            
            assert result == "Generated text from LM Studio"
            mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lmstudio_message_structure(self):
        """Should format messages in OpenAI style."""
        client = LMStudioClient()
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Response"}}]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch.object(client.client, 'post', return_value=mock_response) as mock_post:
            await client.generate("User prompt", system="System message")
            
            call_args = mock_post.call_args[1]['json']
            messages = call_args['messages']
            
            assert len(messages) == 2
            assert messages[0]['role'] == 'system'
            assert messages[0]['content'] == 'System message'
            assert messages[1]['role'] == 'user'
            assert messages[1]['content'] == 'User prompt'
