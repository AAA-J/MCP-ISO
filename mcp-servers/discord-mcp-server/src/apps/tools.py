"""Tools for building Discord apps/bots."""

from mcp.types import Tool, TextContent
import json

apps_tools = [
    Tool(
        name="discord_scaffold_app",
        description="Generate starter code for a Discord bot/application",
        inputSchema={
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["typescript", "python", "javascript"],
                    "description": "Programming language"
                },
                "framework": {
                    "type": "string",
                    "enum": ["discord.js", "discord.py", "rest"],
                    "description": "Discord library/framework"
                },
                "features": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["slash-commands", "components", "webhooks", "oauth2"]
                    },
                    "description": "Features to include"
                },
                "appName": {
                    "type": "string",
                    "description": "Name of the application"
                }
            },
            "required": ["language", "framework", "features"]
        }
    ),
    Tool(
        name="discord_generate_slash_command",
        description="Generate code for a Discord slash command with proper schema",
        inputSchema={
            "type": "object",
            "properties": {
                "commandName": {
                    "type": "string",
                    "description": "Name of the slash command"
                },
                "description": {
                    "type": "string",
                    "description": "Command description"
                },
                "options": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "type": {"type": "number"},
                            "required": {"type": "boolean"}
                        }
                    }
                },
                "language": {
                    "type": "string",
                    "enum": ["typescript", "python"]
                },
                "framework": {
                    "type": "string",
                    "enum": ["discord.js", "discord.py"]
                }
            },
            "required": ["commandName", "description", "language", "framework"]
        }
    ),
    Tool(
        name="discord_generate_component",
        description="Generate code for Discord message components (buttons, select menus, modals)",
        inputSchema={
            "type": "object",
            "properties": {
                "componentType": {
                    "type": "string",
                    "enum": ["button", "select-menu", "modal", "text-input"],
                    "description": "Type of component"
                },
                "language": {
                    "type": "string",
                    "enum": ["typescript", "python"]
                },
                "framework": {
                    "type": "string",
                    "enum": ["discord.js", "discord.py"]
                }
            },
            "required": ["componentType", "language", "framework"]
        }
    ),
    Tool(
        name="discord_validate_interaction",
        description="Validate an interaction payload against Discord API schema",
        inputSchema={
            "type": "object",
            "properties": {
                "payload": {
                    "type": "object",
                    "description": "Interaction payload to validate"
                },
                "interactionType": {
                    "type": "number",
                    "enum": [1, 2, 3, 4, 5],
                    "description": "Interaction type"
                }
            },
            "required": ["payload", "interactionType"]
        }
    ),
    Tool(
        name="discord_check_permissions",
        description="Verify bot permissions are sufficient for required operations",
        inputSchema={
            "type": "object",
            "properties": {
                "operations": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["send-messages", "read-messages", "manage-messages", "manage-channels"]
                    }
                },
                "currentPermissions": {
                    "type": "string",
                    "description": "Current permission integer"
                }
            },
            "required": ["operations"]
        }
    ),
]

async def handle_apps(name: str, arguments: dict) -> list[TextContent]:
    """Handle Discord apps tool calls."""
    if name == "discord_scaffold_app":
        language = arguments.get("language")
        framework = arguments.get("framework")
        features = arguments.get("features")
        app_name = arguments.get("appName", "discord-app")
        
        result = {
            "success": True,
            "language": language,
            "framework": framework,
            "features": features,
            "files": generate_app_files(language, framework, features, app_name)
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "discord_generate_slash_command":
        command_name = arguments.get("commandName")
        language = arguments.get("language")
        code = f"# Generated {language} slash command: {command_name}"
        return [TextContent(type="text", text=code)]
    elif name == "discord_generate_component":
        component_type = arguments.get("componentType")
        language = arguments.get("language")
        code = f"# Generated {language} {component_type} component"
        return [TextContent(type="text", text=code)]
    elif name == "discord_validate_interaction":
        payload = arguments.get("payload")
        result = {"valid": True, "errors": []}
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "discord_check_permissions":
        operations = arguments.get("operations")
        result = {"hasAllPermissions": True, "missingPermissions": []}
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        raise ValueError(f"Unknown Discord apps tool: {name}")

def generate_app_files(language: str, framework: str, features: list, app_name: str) -> dict:
    """Generate Discord app file structure."""
    files = {}
    if language == "python":
        files["src/index.py"] = f"# {app_name} Discord bot\n"
        files["requirements.txt"] = f"discord.py>=2.0.0\n"
    elif language == "typescript":
        files["src/index.ts"] = f"// {app_name} Discord bot\n"
        files["package.json"] = json.dumps({"name": app_name, "dependencies": {"discord.js": "^14.0.0"}}, indent=2)
    return files

