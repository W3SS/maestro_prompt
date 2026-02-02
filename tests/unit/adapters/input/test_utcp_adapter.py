
import pytest
from unittest.mock import MagicMock
import sys

# Mock utcp before importing adapter
mock_utcp = MagicMock()
sys.modules["utcp"] = mock_utcp

from src.adapters.input.utcp.adapter import get_utcp_tools
from src.application.tool_schema import DesignAlbumInput, CreateBatchInput, StartBatchInput

class TestUTCPAdapter:
    """Test suite for UTCP Adapter."""

    def test_get_utcp_tools_returns_list(self):
        """Should return a list of Tool objects."""
        tools = get_utcp_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0
        
    def test_tools_have_correct_metadata(self):
        """Tools should have names and descriptions."""
        # Configure mock to return objects with name attribute matching the input name
        def side_effect(func, name, description, args_model):
            m = MagicMock()
            m.name = name
            m.description = description
            m.args_model = args_model
            return m
            
        mock_utcp.Tool.from_function.side_effect = side_effect
        
        tools = get_utcp_tools()
        design_tool = next(t for t in tools if t.name == "design_album")
        
        assert design_tool is not None
        assert design_tool.description == "Design a concept album using AI."
        assert design_tool.args_model == DesignAlbumInput
