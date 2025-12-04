"""Documentation generation tools for MCP servers."""

from mcp.types import Tool, TextContent
import json

docs_generator_tools = [
    Tool(
        name="generate_api_docs",
        description="Generate API documentation from MCP server code",
        inputSchema={
            "type": "object",
            "properties": {
                "serverPath": {
                    "type": "string",
                    "description": "Path to MCP server source code"
                },
                "outputFormat": {
                    "type": "string",
                    "enum": ["markdown", "html", "json"],
                    "default": "markdown"
                }
            },
            "required": ["serverPath"]
        }
    ),
    Tool(
        name="generate_readme",
        description="Generate README.md from MCP server configuration",
        inputSchema={
            "type": "object",
            "properties": {
                "serverConfig": {
                    "type": "object",
                    "description": "Server configuration object"
                },
                "includeExamples": {
                    "type": "boolean",
                    "default": True
                }
            },
            "required": ["serverConfig"]
        }
    ),
]

async def handle_docs_generator(name: str, arguments: dict) -> list[TextContent]:
    """Handle docs generator tool calls."""
    if name == "generate_api_docs":
        server_path = arguments.get("serverPath")
        output_format = arguments.get("outputFormat", "markdown")
        docs = f"# API Documentation\n\nGenerated from {server_path}\nFormat: {output_format}"
        return [TextContent(type="text", text=docs)]
    elif name == "generate_readme":
        server_config = arguments.get("serverConfig")
        include_examples = arguments.get("includeExamples", True)
        readme = f"# MCP Server\n\nGenerated README\nConfig: {json.dumps(server_config)}"
        return [TextContent(type="text", text=readme)]
    else:
        raise ValueError(f"Unknown docs generator tool: {name}")

