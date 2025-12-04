#!/usr/bin/env python3
"""
Example: Basic usage of Dev-MCP-Server tools
This demonstrates how to use the Dev-MCP-Server programmatically.
"""

import asyncio
import json
from mcp.client.stdio import stdio_client

async def example_scaffold_server():
    """Example: Scaffold a new MCP server."""
    # This would typically be called via MCP client
    # For demonstration purposes:
    print("Example: Scaffold MCP Server")
    print("Tool: scaffold_mcp_server")
    print("Arguments:")
    print(json.dumps({
        "serverName": "my-mcp-server",
        "language": "python",
        "transport": "stdio",
        "features": ["tools", "resources"]
    }, indent=2))

async def example_generate_tool():
    """Example: Generate a tool handler."""
    print("\nExample: Generate Tool Handler")
    print("Tool: generate_tool_handler")
    print("Arguments:")
    print(json.dumps({
        "toolSchema": {
            "name": "get_weather",
            "description": "Get weather information",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location name"
                    }
                },
                "required": ["location"]
            }
        },
        "language": "python"
    }, indent=2))

async def example_validate_schema():
    """Example: Validate a tool schema."""
    print("\nExample: Validate Tool Schema")
    print("Tool: validate_tool_schema")
    print("Arguments:")
    print(json.dumps({
        "toolSchema": {
            "name": "example_tool",
            "description": "An example tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Input value"}
                },
                "required": ["input"]
            }
        },
        "strict": False
    }, indent=2))

if __name__ == "__main__":
    print("Dev-MCP-Server Usage Examples")
    print("=" * 50)
    asyncio.run(example_scaffold_server())
    asyncio.run(example_generate_tool())
    asyncio.run(example_validate_schema())

