"""Integration tests for Unified Server entrypoint."""

import pytest
from unittest.mock import patch, MagicMock
from src.main_server import main
import sys


class TestUnifiedServer:
    """Test suite for main_server CLI."""
    
    def test_api_mode_starts_uvicorn(self):
        """Should start uvicorn when mode is 'api'."""
        test_args = ["main_server.py", "--mode", "api", "--port", "8080"]
        
        with patch.object(sys, 'argv', test_args):
            with patch('src.main_server.start_api_server') as mock_start:
                with patch.object(sys, 'exit'):  # Prevent actual exit
                    try:
                        main()
                    except SystemExit:
                        pass
                
                mock_start.assert_called_once_with(host="0.0.0.0", port=8080)
    
    def test_mcp_mode_starts_mcp_server(self):
        """Should start MCP server when mode is 'mcp'."""
        test_args = ["main_server.py", "--mode", "mcp"]
        
        with patch.object(sys, 'argv', test_args):
            with patch('src.main_server.start_mcp_server') as mock_start:
                with patch.object(sys, 'exit'):
                    try:
                        main()
                    except SystemExit:
                        pass
                
                mock_start.assert_called_once()
    
    def test_default_mode_is_api(self):
        """Should default to API mode when no mode specified."""
        test_args = ["main_server.py"]
        
        with patch.object(sys, 'argv', test_args):
            with patch('src.main_server.start_api_server') as mock_start:
                with patch.object(sys, 'exit'):
                    try:
                        main()
                    except SystemExit:
                        pass
                
                mock_start.assert_called_once()
    
    def test_custom_host_and_port(self):
        """Should accept custom host and port arguments."""
        test_args = ["main_server.py", "--mode", "api", "--host", "127.0.0.1", "--port", "9000"]
        
        with patch.object(sys, 'argv', test_args):
            with patch('src.main_server.start_api_server') as mock_start:
                with patch.object(sys, 'exit'):
                    try:
                        main()
                    except SystemExit:
                        pass
                
                mock_start.assert_called_once_with(host="127.0.0.1", port=9000)
