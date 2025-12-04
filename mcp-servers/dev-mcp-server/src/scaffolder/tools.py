"""Scaffolding tools for generating MCP server projects."""

from mcp.types import Tool, TextContent
import json

scaffolder_tools = [
    Tool(
        name="scaffold_mcp_server",
        description="Generate a new MCP server project with proper structure",
        inputSchema={
            "type": "object",
            "properties": {
                "serverName": {
                    "type": "string",
                    "description": "Name of the MCP server"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript", "javascript"],
                    "description": "Programming language"
                },
                "transport": {
                    "type": "string",
                    "enum": ["stdio", "http", "sse"],
                    "description": "Transport protocol",
                    "default": "stdio"
                },
                "features": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["tools", "resources", "prompts"]
                    },
                    "description": "Features to include"
                },
                "outputPath": {
                    "type": "string",
                    "description": "Output directory path"
                }
            },
            "required": ["serverName", "language", "features"]
        }
    ),
    Tool(
        name="add_tool_template",
        description="Add a new tool template to an existing MCP server",
        inputSchema={
            "type": "object",
            "properties": {
                "toolName": {
                    "type": "string",
                    "description": "Name of the tool"
                },
                "description": {
                    "type": "string",
                    "description": "Tool description"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                },
                "outputPath": {
                    "type": "string",
                    "description": "Path to add the tool"
                }
            },
            "required": ["toolName", "description", "language"]
        }
    ),
    Tool(
        name="add_resource_template",
        description="Add a new resource template to an existing MCP server",
        inputSchema={
            "type": "object",
            "properties": {
                "resourceUri": {
                    "type": "string",
                    "description": "Resource URI pattern"
                },
                "resourceName": {
                    "type": "string",
                    "description": "Resource name"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                },
                "outputPath": {
                    "type": "string"
                }
            },
            "required": ["resourceUri", "resourceName", "language"]
        }
    ),
]

async def handle_scaffolder(name: str, arguments: dict) -> list[TextContent]:
    """Handle scaffolder tool calls."""
    if name == "scaffold_mcp_server":
        server_name = arguments.get("serverName")
        language = arguments.get("language")
        transport = arguments.get("transport", "stdio")
        features = arguments.get("features", [])
        
        # Generate project structure
        structure = {
            "serverName": server_name,
            "language": language,
            "transport": transport,
            "features": features,
            "files": generate_project_files(server_name, language, transport, features)
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(structure, indent=2)
        )]
    elif name == "add_tool_template":
        # Generate tool template
        return [TextContent(
            type="text",
            text=json.dumps({"tool": "template generated"}, indent=2)
        )]
    elif name == "add_resource_template":
        # Generate resource template
        return [TextContent(
            type="text",
            text=json.dumps({"resource": "template generated"}, indent=2)
        )]
    else:
        raise ValueError(f"Unknown scaffolder tool: {name}")

def generate_project_files(server_name: str, language: str, transport: str, features: list) -> dict:
    """Generate project file structure."""
    files = {}
    
    if language == "python":
        files["src/index.py"] = "# MCP Server entry point\n"
        files["requirements.txt"] = "# Dependencies\n"
        if "tools" in features:
            files["src/tools/__init__.py"] = ""
        if "resources" in features:
            files["src/resources/__init__.py"] = ""
        if "prompts" in features:
            files["src/prompts/__init__.py"] = ""
    
    return files

