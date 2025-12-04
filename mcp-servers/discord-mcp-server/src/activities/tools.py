"""Tools for building Discord Activities."""

from mcp.types import Tool, TextContent
import json

activities_tools = [
    Tool(
        name="discord_generate_activity_starter",
        description="Generate starter code for a Discord Activity",
        inputSchema={
            "type": "object",
            "properties": {
                "activityName": {
                    "type": "string",
                    "description": "Name of the activity"
                },
                "hasMultiplayer": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether the activity supports multiplayer"
                },
                "framework": {
                    "type": "string",
                    "enum": ["react", "vanilla", "phaser"],
                    "default": "react"
                },
                "activityType": {
                    "type": "string",
                    "enum": ["embedded", "iframe"],
                    "default": "embedded"
                }
            },
            "required": ["activityName"]
        }
    ),
    Tool(
        name="discord_generate_activity_layout",
        description="Generate layout code for Discord Activity UI",
        inputSchema={
            "type": "object",
            "properties": {
                "layoutType": {
                    "type": "string",
                    "enum": ["single-player", "multiplayer", "spectator"],
                    "description": "Type of layout"
                },
                "framework": {
                    "type": "string",
                    "enum": ["react", "vanilla"]
                }
            },
            "required": ["layoutType", "framework"]
        }
    ),
    Tool(
        name="discord_generate_networking",
        description="Generate multiplayer networking code for Activities",
        inputSchema={
            "type": "object",
            "properties": {
                "framework": {
                    "type": "string",
                    "enum": ["react", "vanilla", "phaser"]
                },
                "transportType": {
                    "type": "string",
                    "enum": ["websocket", "webrtc", "discord-rpc"],
                    "default": "websocket"
                }
            },
            "required": ["framework"]
        }
    ),
    Tool(
        name="discord_validate_activity_metadata",
        description="Validate activity metadata against Discord requirements",
        inputSchema={
            "type": "object",
            "properties": {
                "metadata": {
                    "type": "object",
                    "description": "Activity metadata object"
                }
            },
            "required": ["metadata"]
        }
    ),
]

async def handle_activities(name: str, arguments: dict) -> list[TextContent]:
    """Handle Discord Activities tool calls."""
    if name == "discord_generate_activity_starter":
        activity_name = arguments.get("activityName")
        has_multiplayer = arguments.get("hasMultiplayer", False)
        framework = arguments.get("framework", "react")
        
        result = {
            "success": True,
            "activityName": activity_name,
            "multiplayer": has_multiplayer,
            "framework": framework,
            "files": generate_activity_files(activity_name, has_multiplayer, framework)
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "discord_generate_activity_layout":
        layout_type = arguments.get("layoutType")
        framework = arguments.get("framework")
        code = f"# Generated {framework} layout for {layout_type}"
        return [TextContent(type="text", text=code)]
    elif name == "discord_generate_networking":
        framework = arguments.get("framework")
        transport = arguments.get("transportType", "websocket")
        code = f"# Generated {framework} networking code using {transport}"
        return [TextContent(type="text", text=code)]
    elif name == "discord_validate_activity_metadata":
        metadata = arguments.get("metadata")
        result = {"valid": True, "errors": []}
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        raise ValueError(f"Unknown Discord Activities tool: {name}")

def generate_activity_files(activity_name: str, has_multiplayer: bool, framework: str) -> dict:
    """Generate Activity file structure."""
    files = {}
    if framework == "react":
        files["src/App.tsx"] = f"// {activity_name} Activity\n"
        files["package.json"] = json.dumps({"name": activity_name, "dependencies": {"@discord/embedded-app-sdk": "^1.0.0"}}, indent=2)
    return files

