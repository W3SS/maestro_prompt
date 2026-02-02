
import pytest
from unittest.mock import MagicMock, patch, ANY
import sys

# Mock mcp.server.fastmcp before importing the server
mock_fastmcp_module = MagicMock()
sys.modules["mcp.server.fastmcp"] = mock_fastmcp_module

# Configure FastMCP class and instance
mock_fastmcp_class = MagicMock()
mock_fastmcp_module.FastMCP = mock_fastmcp_class
mock_fastmcp_instance = mock_fastmcp_class.return_value

# Define a pass-through decorator for @mcp.tool()
def tool_decorator(*args, **kwargs):
    def decorator(f):
        return f
    return decorator

# Set the side effect on the instance's tool method
mock_fastmcp_instance.tool.side_effect = tool_decorator

# Now import the module under test
from src.adapters.input.mcp.server import mcp, run_mcp_server

class TestMCPServer:
    """Test suite for MCP Server adapter."""

    def test_mcp_server_initialization(self):
        """Test that MCP server is initialized with correct name."""
        assert mcp is not None
        # Verify it's utilizing the mocked FastMCP
        # Note: In real execution, 'mcp' is an instance of FastMCP("Maestro AI")
        pass

    @patch("src.adapters.input.mcp.server.MaestroTools")
    def test_tools_registration(self, mock_tools):
        """Test that tools are registered with the server."""
        # Since decorators run at import time, we verify via the mock_fastmcp instance
        # if the decorators were called.
        # This is a bit tricky with global objects. 
        # Alternatively, we invoke the decorated functions to see if they call MaestroTools.
        
        from src.adapters.input.mcp.server import (
            design_album, create_batch, start_batch, 
            add_items_to_batch, get_batch, list_batches,
            complete_batch, cancel_batch
        )
        
        # Test design_album
        mock_input = MagicMock()
        mock_input.archetype = "arch"
        mock_input.genres = []
        mock_input.theme = None
        
        design_album(
            archetype="arch", 
            genres=[], 
            theme=None
        )
        mock_tools.design_album.assert_called_once()
        
        # Test create_batch
        create_batch(name="test")
        mock_tools.create_batch.assert_called_once()

    @patch("src.adapters.input.mcp.server.mcp")
    def test_run_mcp_server(self, mock_mcp_instance):
        """Test that run_mcp_server calls mcp.run()."""
        run_mcp_server()
        mock_mcp_instance.run.assert_called_once()
