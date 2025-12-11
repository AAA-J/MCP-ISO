#!/usr/bin/env python3
"""
App-Docs MCP Server - Internal documentation access
Makes all internal docs and specs easily accessible to agents
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent

from docs_reader.tools import discover_docs, read_doc_resource
from search.tools import search_tools, handle_search

# Load environment variables
load_dotenv()

# Initialize MCP server
server = Server("app-docs")

# Get configuration
DOCS_DIR = os.getenv("DOCS_DIR", "docs")
BASE_DIR = os.getenv("BASE_DIR", os.getcwd())
docs_path = Path(BASE_DIR) / DOCS_DIR


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return search_tools


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name in ["search_docs", "get_diagram"]:
        return await handle_search(name, arguments, str(docs_path))
    else:
        raise ValueError(f"Unknown tool: {name}")


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available documentation resources."""
    return discover_docs(str(docs_path))


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a documentation resource."""
    uri_str = str(uri)
    return await read_doc_resource(uri_str, str(docs_path))


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

