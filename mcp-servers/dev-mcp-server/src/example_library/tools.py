"""Example library tools for MCP servers."""

from mcp.types import Tool, TextContent
import json

example_library_tools = [
    Tool(
        name="get_example_server",
        description="Get example MCP server code",
        inputSchema={
            "type": "object",
            "properties": {
                "exampleType": {
                    "type": "string",
                    "enum": ["basic", "with-auth", "multi-transport", "error-handling"],
                    "description": "Type of example server"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                }
            },
            "required": ["exampleType", "language"]
        }
    ),
    Tool(
        name="get_pattern",
        description="Get common MCP development patterns",
        inputSchema={
            "type": "object",
            "properties": {
                "patternName": {
                    "type": "string",
                    "enum": ["authentication", "error-handling", "rate-limiting", "logging"],
                    "description": "Pattern name"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                }
            },
            "required": ["patternName", "language"]
        }
    ),
]

async def handle_example_library(name: str, arguments: dict) -> list[TextContent]:
    """Handle example library tool calls."""
    if name == "get_example_server":
        example_type = arguments.get("exampleType")
        language = arguments.get("language")
        example = {
            "type": example_type,
            "language": language,
            "code": f"# Example {example_type} server in {language}"
        }
        return [TextContent(type="text", text=json.dumps(example, indent=2))]
    elif name == "get_pattern":
        pattern_name = arguments.get("patternName")
        language = arguments.get("language")
        pattern = {
            "pattern": pattern_name,
            "language": language,
            "code": f"# {pattern_name} pattern in {language}"
        }
        return [TextContent(type="text", text=json.dumps(pattern, indent=2))]
    else:
        raise ValueError(f"Unknown example library tool: {name}")

