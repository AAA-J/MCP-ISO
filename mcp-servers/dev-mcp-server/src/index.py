#!/usr/bin/env python3
"""
Dev-MCP-Server - MCP server for building MCP servers
"""

import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent

# Import tool modules
from spec_reference.tools import spec_reference_tools, handle_spec_reference
from scaffolder.tools import scaffolder_tools, handle_scaffolder
from code_generator.tools import code_generator_tools, handle_code_generator
from validator.tools import validator_tools, handle_validator
from tester.tools import tester_tools, handle_tester
from example_library.tools import example_library_tools, handle_example_library
from docs_generator.tools import docs_generator_tools, handle_docs_generator
from deployment_helper.tools import deployment_helper_tools, handle_deployment_helper
from package_manager.tools import package_manager_tools, handle_package_manager

# Initialize MCP server
server = Server("dev-mcp-server")

# Combine all tools
all_tools = (
    spec_reference_tools +
    scaffolder_tools +
    code_generator_tools +
    validator_tools +
    tester_tools +
    example_library_tools +
    docs_generator_tools +
    deployment_helper_tools +
    package_manager_tools
)

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return all_tools

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    # Route to appropriate handler based on tool name prefix
    if name.startswith("spec_"):
        return await handle_spec_reference(name, arguments)
    elif name.startswith("scaffold_") or name.startswith("add_"):
        return await handle_scaffolder(name, arguments)
    elif name.startswith("generate_"):
        if name.startswith("generate_docs") or name.startswith("generate_readme"):
            return await handle_docs_generator(name, arguments)
        return await handle_code_generator(name, arguments)
    elif name.startswith("validate_"):
        return await handle_validator(name, arguments)
    elif name.startswith("test_"):
        return await handle_tester(name, arguments)
    elif name.startswith("get_example") or name.startswith("get_pattern"):
        return await handle_example_library(name, arguments)
    elif name.startswith("check_") or name.startswith("suggest_"):
        return await handle_package_manager(name, arguments)
    elif name.startswith("deploy_") or name.startswith("dockerfile"):
        return await handle_deployment_helper(name, arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="mcp://spec/overview",
            name="MCP Specification Overview",
            description="MCP specification overview",
            mimeType="text/markdown"
        ),
        Resource(
            uri="mcp://examples/basic",
            name="Basic Server Example",
            description="Basic MCP server example",
            mimeType="application/json"
        ),
        Resource(
            uri="mcp://patterns/auth",
            name="Authentication Patterns",
            description="Common authentication patterns",
            mimeType="text/markdown"
        ),
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource."""
    if uri.startswith("mcp://spec/"):
        # Return spec reference content
        return "# MCP Specification\n\nSpecification content..."
    elif uri.startswith("mcp://examples/"):
        # Return example code
        return '{"example": "code"}'
    elif uri.startswith("mcp://patterns/"):
        # Return pattern documentation
        return "# Pattern Documentation\n\nPattern content..."
    else:
        raise ValueError(f"Unknown resource: {uri}")

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

