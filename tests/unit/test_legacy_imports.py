
import pytest

class TestLegacyImports:
    """Test suite for backward compatibility modules."""

    def test_llm_client_exports(self):
        """Should re-export LLM classes."""
        from src.llm_client import LLMClient, LLMConfig, LLMError
        assert LLMClient is not None
        assert LLMConfig is not None
        assert LLMError is not None

    def test_context_manager_exports(self):
        """Should re-export Context Manager classes."""
        from src.context_manager import ContextManager, ContextConfig, ContextError
        assert ContextManager is not None
        assert ContextConfig is not None
        assert ContextError is not None
