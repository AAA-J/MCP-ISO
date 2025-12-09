#!/usr/bin/env python3
"""
Dev-MCP-Server - MCP server for building MCP servers
"""

import asyncio
import json
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
    # Convert URI to string if it's an AnyUrl object
    uri_str = str(uri)
    
    if uri_str.startswith("mcp://spec/"):
        # Import spec content
        from spec_reference.tools import MCP_SPEC_CONTENT
        
        topic = uri_str.replace("mcp://spec/", "")
        if topic == "overview":
            return "# MCP Specification Overview\n\n" + "\n\n".join([
                f"## {t}\n\n{MCP_SPEC_CONTENT[t]['overview'][:500]}..." 
                for t in MCP_SPEC_CONTENT.keys()
            ])
        elif topic in MCP_SPEC_CONTENT:
            return MCP_SPEC_CONTENT[topic]["overview"]
        else:
            return "# MCP Specification\n\nAvailable topics: " + ", ".join(MCP_SPEC_CONTENT.keys())
    
    elif uri_str.startswith("mcp://examples/"):
        # Import example content
        from example_library.tools import EXAMPLES
        
        example_type = uri_str.replace("mcp://examples/", "")
        if example_type == "basic":
            return EXAMPLES["basic"]["python"]
        elif example_type in EXAMPLES:
            return json.dumps(EXAMPLES[example_type], indent=2)
        else:
            return json.dumps({"available": list(EXAMPLES.keys())}, indent=2)
    
    elif uri_str.startswith("mcp://patterns/"):
        # Import pattern content
        from example_library.tools import PATTERNS
        
        pattern_name = uri_str.replace("mcp://patterns/", "")
        if pattern_name == "auth":
            pattern_name = "authentication"
        
        if pattern_name in PATTERNS:
            return PATTERNS[pattern_name]["python"]
        else:
            return "# Patterns\n\nAvailable patterns: " + ", ".join(PATTERNS.keys())
    
    else:
        raise ValueError(f"Unknown resource: {uri_str}")

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

