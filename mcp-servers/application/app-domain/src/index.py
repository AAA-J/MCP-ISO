#!/usr/bin/env python3
"""
App-Domain MCP Server - Business logic shortcuts
Provides domain-specific tools for business operations
"""

import asyncio
import os
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from domain.tools import (
    load_domain_tools,
    handle_domain_tool,
    default_domain_tools
)

# Load environment variables
load_dotenv()

# Initialize MCP server
server = Server("app-domain")

# Configuration
DOMAIN_TOOLS_CONFIG = os.getenv("DOMAIN_TOOLS_CONFIG", "domain_tools.yaml")
API_BASE_URL = os.getenv("API_BASE_URL")  # Optional, for API-based tools

# Authentication configuration
AUTH_TYPE = os.getenv("AUTH_TYPE", "bearer").lower()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME", "X-API-Key")

auth_config = {
    "type": AUTH_TYPE,
    "token": AUTH_TOKEN,
    "api_key": API_KEY,
    "key_name": API_KEY_NAME
} if AUTH_TOKEN or API_KEY else None

# Load domain tools configuration
tool_config = {}
domain_tools = default_domain_tools.copy()

if os.path.exists(DOMAIN_TOOLS_CONFIG):
    try:
        import yaml
        with open(DOMAIN_TOOLS_CONFIG, 'r') as f:
            tool_config = yaml.safe_load(f) or {}
        
        # Load tools from config
        config_tools = load_domain_tools(DOMAIN_TOOLS_CONFIG)
        domain_tools.extend(config_tools)
    except Exception as e:
        print(f"Warning: Could not load domain tools config: {e}")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available domain tools."""
    return domain_tools


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    
    # Handle default generic tool
    if name == "execute_domain_action":
        action = arguments.get("action")
        params = arguments.get("params", {})
        
        if not action:
            return [TextContent(
                type="text",
                text="Error: Action name is required"
            )]
        
        # Try to find a configured tool matching the action
        for tool in tool_config.get("tools", []):
            if tool.get("name") == action:
                return await handle_domain_tool(
                    action,
                    params,
                    tool_config,
                    API_BASE_URL,
                    auth_config
                )
        
        return [TextContent(
            type="text",
            text=f"Domain action '{action}' not found in configuration"
        )]
    
    # Handle configured domain tools
    return await handle_domain_tool(
        name,
        arguments,
        tool_config,
        API_BASE_URL,
        auth_config
    )


async def main():
    """Main entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

