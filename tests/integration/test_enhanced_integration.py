"""
Integration tests for enhanced album design workflow.

NOTE: These tests require the full application stack and are skipped in CI.
They test the end-to-end flow with real LLM and context loading.
"""

import pytest

# Skip all integration tests in CI (they require legacy modules being refactored)
pytestmark = pytest.mark.skip(reason="Legacy integration tests - being refactored to new architecture")


def test_placeholder():
    """Placeholder test to prevent collection errors."""
    pass
