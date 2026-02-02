"""
Backward compatibility layer for old imports.

This module maintains compatibility with existing tests
while we transition to hexagonal architecture.
"""

# Re-export from new locations for backward compatibility
from src.adapters.output.llm.ollama_adapter import (
    LLMClient,
    LLMConfig,
    LLMError,
    TimeoutError,
    RetryError
)

from src.adapters.output.context.json_context_adapter import (
    ContextManager,
    ContextConfig,
    ContextError
)

__all__ = [
    # LLM Client
    "LLMClient",
    "LLMConfig",
    "LLMError",
    "TimeoutError",
    "RetryError",
    # Context Manager
    "ContextManager",
    "ContextConfig",
    "ContextError",
]
