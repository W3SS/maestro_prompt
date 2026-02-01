# MCP Server Configuration for Claude Desktop / Continue

This document explains how to integrate Maestro AI MCP Server with MCP clients.

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "maestro-ai": {
      "command": "python",
      "args": ["-m", "src.adapters.input.mcp.server"],
      "cwd": "h:/Meu Drive/codebase/tech/maestro_prompt"
    }
  }
}
```

## Continue Integration

Add to `.continue/config.json`:

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "python",
          "args": ["-m", "src.adapters.input.mcp.server"],
          "cwd": "h:/Meu Drive/codebase/tech/maestro_prompt"
        }
      }
    ]
  }
}
```

## Available Tools (8 total)

### Album Design
- `design_album` - Generate concept album with AI

### Batch Management
- `create_batch` - Create new Suno batch
- `add_items_to_batch` - Add tracks to batch
- `get_batch` - Get batch details
- `list_batches` - List all batches (filterable)

### Batch Operations
- `start_batch` - Start processing
- `complete_batch` - Mark as completed
- `cancel_batch` - Cancel batch

## Testing

```bash
# Test MCP server directly
python -m src.adapters.input.mcp.server
```

## Dependencies

Ensure `mcp` is installed:
```bash
pip install mcp
```
