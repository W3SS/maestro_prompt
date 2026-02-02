import pytest
import subprocess
import sys
import asyncio
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


class TestServerFunctions:
    """Test suite for server start functions executing their bodies."""

    def test_start_api_server_runs_uvicorn(self):
        """test_start_api_server should import uvicorn and run it."""
        mock_uvicorn = MagicMock()
        mock_app = MagicMock()
        
        # We need to mock the imports execution inside the function
        with patch.dict(sys.modules, {
            "uvicorn": mock_uvicorn,
            "src.adapters.input.api.main": MagicMock(app=mock_app)
        }):
            # We also need to patch builtins print to avoid clutter
            with patch("builtins.print"):
                start_api_server(host="1.2.3.4", port=9999)
        
        mock_uvicorn.run.assert_called_once_with(mock_app, host="1.2.3.4", port=9999, log_level="info")

    def test_start_mcp_server_runs_mcp(self):
        """test_start_mcp_server should import run_mcp_server and run it."""
        mock_run_mcp = MagicMock()
        
        with patch.dict(sys.modules, {
            "src.adapters.input.mcp.server": MagicMock(run_mcp_server=mock_run_mcp)
        }):
            with patch("builtins.print"):
                start_mcp_server()
                
        mock_run_mcp.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_all_servers_concurrently(self):
        """test_start_all_servers should create tasks for api and run mcp."""
        mock_uvicorn = MagicMock()
        mock_app = MagicMock()
        mock_mcp = MagicMock()
        
        # We need to mock asyncio.gather to avoid actual waiting/execution in test
        # But we want to verify the tasks were created.
        
        with patch.dict(sys.modules, {
            "uvicorn": mock_uvicorn,
            "src.adapters.input.api.main": MagicMock(app=mock_app),
            "src.adapters.input.mcp.server": MagicMock(mcp=mock_mcp)
        }):
            with patch("builtins.print"):
                # We spy on asyncio.create_task or to_thread
                with patch("asyncio.to_thread", new_callable=AsyncMock) as mock_to_thread:
                     with patch("asyncio.gather", new_callable=AsyncMock) as mock_gather:
                        save_create_task = asyncio.create_task
                        # We need actual create_task probably, or mock it too.
                        # Using real create_task might require real event loop which pytest-asyncio provides.
                        
                        await start_all_servers(host="1.1.1.1", port=5555)
                        
                        # Verify to_thread was called for uvicorn and mcp.run
                        # args for uvicorn: uvicorn.run, app, ...
                        # args for mcp: mcp.run
                        
                        calls = mock_to_thread.call_args_list
                        
                        # We expect 2 calls
                        assert len(calls) == 2
                        
                        # Check calls args
                        # One should be for uvicorn
                        uvicorn_called = any(c.args[0] == mock_uvicorn.run for c in calls)
                        mcp_called = any(c.args[0] == mock_mcp.run for c in calls)
                        
                        assert uvicorn_called, "Uvicorn run task should be created"
                        assert mcp_called, "MCP run task should be created"
                        
                        mock_gather.assert_awaited_once()

