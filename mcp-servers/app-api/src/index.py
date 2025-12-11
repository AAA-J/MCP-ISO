#!/usr/bin/env python3
"""
App-API MCP Server - Backend API wrapper
Provides typed tools for interacting with backend APIs
"""

import asyncio
import os
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from api_client.tools import (
    default_tools,
    load_tool_config,
    build_tools_from_config,
    handle_api_tool
)

# Load environment variables
load_dotenv()

# Initialize MCP server
server = Server("app-api")

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TYPE = os.getenv("API_TYPE", "rest").lower()  # rest, graphql, fastapi, express
TOOL_CONFIG_FILE = os.getenv("TOOL_CONFIG_FILE")  # Optional YAML/JSON config

# Authentication configuration
AUTH_TYPE = os.getenv("AUTH_TYPE", "bearer").lower()  # bearer, api_key, basic
AUTH_TOKEN = os.getenv("AUTH_TOKEN")  # For bearer token
API_KEY = os.getenv("API_KEY")  # For API key auth
API_KEY_NAME = os.getenv("API_KEY_NAME", "X-API-Key")  # Header name for API key
AUTH_USERNAME = os.getenv("AUTH_USERNAME")  # For basic auth
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")  # For basic auth

# Build auth config
auth_config = {
    "type": AUTH_TYPE,
    "token": AUTH_TOKEN,
    "api_key": API_KEY,
    "key_name": API_KEY_NAME,
    "username": AUTH_USERNAME,
    "password": AUTH_PASSWORD
}

# Load tool configuration
tool_config = load_tool_config(TOOL_CONFIG_FILE)
custom_tools = build_tools_from_config(tool_config, API_BASE_URL)

# Combine default and custom tools
all_tools = default_tools + custom_tools


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return all_tools


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    return await handle_api_tool(
        name,
        arguments,
        API_BASE_URL,
        auth_config,
        API_TYPE
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

