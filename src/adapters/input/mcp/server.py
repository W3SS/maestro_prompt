"""
MCP Server for Maestro AI (FastMCP Implementation).

Exposes all 8 Maestro tools via Model Context Protocol,
making them callable from Claude Desktop, Continue, and other MCP clients.
"""

from mcp.server.fastmcp import FastMCP
from typing import List, Optional, Dict, Any
from src.application.tools import MaestroTools
from src.application.tool_schema import (
    DesignAlbumInput, CreateBatchInput, AddItemsInput,
    StartBatchInput, GetBatchInput, ListBatchesInput,
    CompleteBatchInput, CancelBatchInput
)

# Initialize FastMCP server
mcp = FastMCP(
    "Maestro AI",
    dependencies=[]
)

# ===== ALBUM DESIGN =====
@mcp.tool()
def design_album(
    archetype: str,
    genres: List[str],
    theme: Optional[str] = None
) -> dict:
    """
    Design a complete concept album using AI.
    
    Args:
        archetype: Narrative archetype (e.g., 'concept_album', 'cosmic_horror')
        genres: List of musical genres (e.g., ['metal', 'progressive'])
        theme: Optional theme for the album
    
    Returns:
        Album with title and generated tracks
    """
    input_data = DesignAlbumInput(archetype=archetype, genres=genres, theme=theme)
    result = MaestroTools.design_album(input_data)
    return result.model_dump()

# ===== BATCH MANAGEMENT =====
@mcp.tool()
def create_batch(name: str) -> dict:
    """
    Create a new Suno generation batch.
    
    Args:
        name: Batch name
    
    Returns:
        Batch ID and initial status
    """
    input_data = CreateBatchInput(name=name)
    result = MaestroTools.create_batch(input_data)
    return result.model_dump()

@mcp.tool()
def add_items_to_batch(batch_id: str, items: List[Dict[str, Any]]) -> dict:
    """
    Add tracks to an existing batch.
    
    Args:
        batch_id: Batch ID
        items: List of items with prompt, style_tags, and title
    
    Returns:
        Updated batch info with items count
    """
    input_data = AddItemsInput(batch_id=batch_id, items=items)
    result = MaestroTools.add_items_to_batch(input_data)
    return result.model_dump()

@mcp.tool()
def get_batch(batch_id: str) -> dict:
    """
    Get batch details by ID.
    
    Args:
        batch_id: Batch ID
    
    Returns:
        Complete batch information
    """
    input_data = GetBatchInput(batch_id=batch_id)
    result = MaestroTools.get_batch(input_data)
    return result.model_dump()

@mcp.tool()
def list_batches(status: Optional[str] = None) -> dict:
    """
    List all batches, optionally filtered by status.
    
    Args:
        status: Filter by status (pending/processing/completed/failed/cancelled)
    
    Returns:
        List of batches with summary info
    """
    input_data = ListBatchesInput(status=status)
    result = MaestroTools.list_batches(input_data)
    return result.model_dump()

# ===== BATCH OPERATIONS =====
@mcp.tool()
def start_batch(batch_id: str) -> dict:
    """
    Start processing a batch.
    
    Args:
        batch_id: Batch ID
    
    Returns:
        Updated batch status
    """
    input_data = StartBatchInput(batch_id=batch_id)
    result = MaestroTools.start_batch(input_data)
    return result

@mcp.tool()
def complete_batch(batch_id: str) -> dict:
    """
    Mark batch as completed.
    
    Args:
        batch_id: Batch ID
    
    Returns:
        Completion confirmation with timestamp
    """
    input_data = CompleteBatchInput(batch_id=batch_id)
    result = MaestroTools.complete_batch(input_data)
    return result.model_dump()

@mcp.tool()
def cancel_batch(batch_id: str) -> dict:
    """
    Cancel a batch.
    
    Args:
        batch_id: Batch ID
    
    Returns:
        Cancellation confirmation
    """
    input_data = CancelBatchInput(batch_id=batch_id)
    result = MaestroTools.cancel_batch(input_data)
    return result.model_dump()

# ===== SERVER ENTRYPOINT =====
def run_mcp_server():
    """Start the MCP server (stdio mode for Claude Desktop)."""
    mcp.run()

if __name__ == "__main__":
    run_mcp_server()
