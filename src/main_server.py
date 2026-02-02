"""
Unified Server Entrypoint for Maestro AI.

Starts the requested interface(s):
- API: FastAPI HTTP server
- MCP: Model Context Protocol server (stdio)
- ALL: Both API and MCP concurrently
"""

import sys
import argparse
import asyncio
from typing import Literal

ServerMode = Literal["api", "mcp", "all"]

def start_api_server(host: str = "0.0.0.0", port: int = 8000):
    """Start FastAPI server."""
    import uvicorn
    from src.adapters.input.api.main import app
    
    print(f"🚀 Starting FastAPI server on http://{host}:{port}")
    print(f"📚 Swagger docs: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port, log_level="info")

def start_mcp_server():
    """Start MCP server (stdio mode)."""
    from src.adapters.input.mcp.server import run_mcp_server
    
    print("🔌 Starting MCP server (stdio mode)")
    print("💡 Use with Claude Desktop or Continue")
    
    run_mcp_server()

async def start_all_servers(host: str = "0.0.0.0", port: int = 8000):
    """Start both API and MCP servers concurrently."""
    import uvicorn
    from src.adapters.input.api.main import app
    from src.adapters.input.mcp.server import mcp
    
    print("🚀 Starting ALL servers (API + MCP)")
    print(f"📚 FastAPI: http://{host}:{port}/docs")
    print("🔌 MCP: stdio mode")
    
    # Create tasks
    api_task = asyncio.create_task(
        asyncio.to_thread(uvicorn.run, app, host=host, port=port, log_level="info")
    )
    
    # MCP runs in stdio, so it blocks
    # We run API in background and MCP in foreground
    await api_task

def main():
    """Main entrypoint with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Maestro AI - Neural Audio Workstation Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
                python -m src.main_server --mode api              # Start FastAPI only
                python -m src.main_server --mode mcp              # Start MCP only
                python -m src.main_server --mode all              # Start both
                python -m src.main_server --mode api --port 8080  # Custom port
        """
    )
    
    parser.add_argument(
        "--mode",
        type=str,
        choices=["api", "mcp", "all"],
        default="api",
        help="Server mode to start (default: api)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind API server (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for API server (default: 8000)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎹 MAESTRO AI - Neural Audio Workstation")
    print("=" * 60)
    print(f"Mode: {args.mode.upper()}")
    
    try:
        if args.mode == "api":
            start_api_server(host=args.host, port=args.port)
        
        elif args.mode == "mcp":
            start_mcp_server()
        
        elif args.mode == "all":
            asyncio.run(start_all_servers(host=args.host, port=args.port))
    
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
