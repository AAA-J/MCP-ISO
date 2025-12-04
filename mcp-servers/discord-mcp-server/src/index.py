#!/usr/bin/env python3
"""
Discord-MCP-Server - MCP server for Discord development
Helps developers build Discord apps, Activities, and Social SDK integrations
"""

import asyncio
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent

# Import tool modules
from apps.tools import apps_tools, handle_apps
from activities.tools import activities_tools, handle_activities
from social_sdk.tools import social_sdk_tools, handle_social_sdk

# Initialize MCP server
server = Server("discord-mcp-server")

# Combine all tools
all_tools = apps_tools + activities_tools + social_sdk_tools

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return all_tools

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    # Route to appropriate handler based on tool name prefix
    if name.startswith("discord_scaffold_app") or name.startswith("discord_generate_slash") or \
       name.startswith("discord_generate_component") or name.startswith("discord_validate_interaction") or \
       name.startswith("discord_check_permissions"):
        return await handle_apps(name, arguments)
    elif name.startswith("discord_generate_activity") or name.startswith("discord_validate_activity"):
        return await handle_activities(name, arguments)
    elif name.startswith("discord_generate_sdk") or name.startswith("discord_create_account") or \
         name.startswith("discord_generate_rich") or name.startswith("discord_validate_oauth"):
        return await handle_social_sdk(name, arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="discord://docs/interactions",
            name="Discord Interactions Documentation",
            description="Complete guide to Discord interactions",
            mimeType="text/markdown"
        ),
        Resource(
            uri="discord://docs/activities",
            name="Discord Activities Documentation",
            description="Complete guide to building Discord Activities",
            mimeType="text/markdown"
        ),
        Resource(
            uri="discord://docs/social-sdk",
            name="Discord Social SDK Documentation",
            description="Complete guide to Discord Social SDK",
            mimeType="text/markdown"
        ),
        Resource(
            uri="discord://examples/slash-commands",
            name="Slash Command Examples",
            description="Code examples for slash commands",
            mimeType="application/json"
        ),
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource."""
    if uri.startswith("discord://docs/"):
        # Return documentation reference
        topic = uri.replace("discord://docs/", "")
        return f"# Discord {topic.title()} Documentation\n\nSee docs/DISCORD_DEV_DOCS.md for full documentation."
    elif uri.startswith("discord://examples/"):
        # Return example code
        example_type = uri.replace("discord://examples/", "")
        return '{"example": "' + example_type + '", "code": "// Example code here"}'
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

