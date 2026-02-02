"""Integration tests for Unified Server entrypoint."""

import pytest
import subprocess
import sys
from unittest.mock import patch, MagicMock, AsyncMock
from src.main_server import (
    main, start_api_server, start_mcp_server, start_all_servers
)


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

    def test_all_mode_starts_both_servers(self):
        """Should start both API and MCP when mode is 'all'."""
        test_args = ["main_server.py", "--mode", "all"]
        
        with patch.object(sys, 'argv', test_args):
            with patch('src.main_server.asyncio.run') as mock_asyncio_run:
                with patch.object(sys, 'exit'):
                    try:
                        main()
                    except SystemExit:
                        pass
                
                mock_asyncio_run.assert_called_once()

    def test_keyboard_interrupt_handling(self):
        """Should handle KeyboardInterrupt gracefully."""
        test_args = ["main_server.py", "--mode", "api"]
        
        with patch.object(sys, 'argv', test_args):
            with patch('src.main_server.start_api_server', side_effect=KeyboardInterrupt):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                
                assert exc_info.value.code == 0

    def test_exception_handling(self):
        """Should handle exceptions and exit with code 1."""
        test_args = ["main_server.py", "--mode", "api"]
        
        with patch.object(sys, 'argv', test_args):
            with patch('src.main_server.start_api_server', side_effect=Exception("Test error")):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                
                assert exc_info.value.code == 1


class TestSubprocessExecution:
    """Test the module can be executed as a script."""
    
    def test_module_execution_help(self):
        """Should display help when --help is passed."""
        result = subprocess.run(
            [sys.executable, "-m", "src.main_server", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        assert "Maestro AI" in result.stdout
        assert "--mode" in result.stdout
        assert "--host" in result.stdout
        assert "--port" in result.stdout

