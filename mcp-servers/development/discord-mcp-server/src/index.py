#!/usr/bin/env python3
"""
Discord-MCP-Server - MCP server for Discord development
Helps developers build Discord apps, Activities, and Social SDK integrations
"""

import asyncio
import os
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent

# Import tool modules
from apps.tools import apps_tools, handle_apps
from activities.tools import activities_tools, handle_activities
from social_sdk.tools import social_sdk_tools, handle_social_sdk
from webhooks.tools import webhooks_tools, handle_webhooks

# Initialize MCP server
server = Server("discord-mcp-server")

# Combine all tools
all_tools = apps_tools + activities_tools + social_sdk_tools + webhooks_tools

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
    elif name.startswith("discord_generate_webhook") or name.startswith("discord_generate_oauth2"):
        return await handle_webhooks(name, arguments)
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
            uri="discord://docs/components",
            name="Discord Components Documentation",
            description="Guide to Discord message components",
            mimeType="text/markdown"
        ),
        Resource(
            uri="discord://docs/webhooks",
            name="Discord Webhooks Documentation",
            description="Guide to Discord webhooks",
            mimeType="text/markdown"
        ),
        Resource(
            uri="discord://docs/oauth2",
            name="Discord OAuth2 Documentation",
            description="Guide to Discord OAuth2",
            mimeType="text/markdown"
        ),
        Resource(
            uri="discord://docs/rich-presence",
            name="Discord Rich Presence Documentation",
            description="Guide to Discord Rich Presence",
            mimeType="text/markdown"
        ),
        Resource(
            uri="discord://examples/slash-commands",
            name="Slash Command Examples",
            description="Code examples for slash commands",
            mimeType="application/json"
        ),
        Resource(
            uri="discord://examples/components",
            name="Component Examples",
            description="Code examples for Discord components",
            mimeType="application/json"
        ),
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource."""
    import os
    
    # Convert URI to string if it's an AnyUrl object
    uri_str = str(uri)
    
    if uri_str.startswith("discord://docs/"):
        # Return documentation reference with links
        topic = uri_str.replace("discord://docs/", "").replace("-", " ").title()
        topic_slug = uri_str.replace("discord://docs/", "")
        
        # Try to read from DISCORD_DEV_DOCS.md
        docs_path = os.path.join(os.path.dirname(__file__), "..", "docs", "DISCORD_DEV_DOCS.md")
        if os.path.exists(docs_path):
            with open(docs_path, "r", encoding="utf-8") as f:
                docs_content = f.read()
                # Extract relevant section
                if topic_slug in docs_content.lower():
                    return f"# Discord {topic} Documentation\n\n{docs_content}\n\nFor complete documentation, see: https://discord.com/developers/docs"
        
        # Fallback to topic-specific content
        doc_links = {
            "interactions": "https://discord.com/developers/docs/interactions/overview",
            "activities": "https://discord.com/developers/docs/activities/overview",
            "social-sdk": "https://discord.com/developers/docs/discord-social-sdk/overview",
            "components": "https://discord.com/developers/docs/components/overview",
            "webhooks": "https://discord.com/developers/docs/resources/webhook",
            "oauth2": "https://discord.com/developers/docs/topics/oauth2",
            "rich-presence": "https://discord.com/developers/docs/rich-presence/overview",
        }
        
        link = doc_links.get(topic_slug, "https://discord.com/developers/docs")
        return f"# Discord {topic} Documentation\n\nSee the official Discord Developer Documentation:\n{link}\n\nFor complete reference, see docs/DISCORD_DEV_DOCS.md"
    
    elif uri_str.startswith("discord://examples/"):
        # Return example code
        example_type = uri_str.replace("discord://examples/", "")
        
        examples = {
            "slash-commands": {
                "python": '''import discord
from discord import app_commands
from discord.ext import commands

class PingCommand(commands.Cog):
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Latency: {latency}ms")''',
                "typescript": '''import { SlashCommandBuilder, ChatInputCommandInteraction } from 'discord.js';

export const data = new SlashCommandBuilder()
    .setName('ping')
    .setDescription('Check bot latency');

export async function execute(interaction: ChatInputCommandInteraction) {
    const latency = Math.round(interaction.client.ws.ping);
    await interaction.reply(`Pong! Latency: ${latency}ms`);
}'''
            },
            "components": {
                "python": '''import discord
from discord import ui

class ButtonView(ui.View):
    @ui.button(label='Click Me!', style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message('Button clicked!', ephemeral=True)''',
                "typescript": '''import { ActionRowBuilder, ButtonBuilder, ButtonStyle } from 'discord.js';

const row = new ActionRowBuilder<ButtonBuilder>()
    .addComponents(
        new ButtonBuilder()
            .setCustomId('example_button')
            .setLabel('Click Me!')
            .setStyle(ButtonStyle.Primary)
    );'''
            }
        }
        
        if example_type in examples:
            return json.dumps(examples[example_type], indent=2)
        return json.dumps({"example": example_type, "code": "// Example code here"}, indent=2)
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

