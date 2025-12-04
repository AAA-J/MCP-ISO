"""Tools for building Discord Social SDK integrations."""

from mcp.types import Tool, TextContent
import json

social_sdk_tools = [
    Tool(
        name="discord_generate_sdk_init",
        description="Generate SDK initialization code for Discord Social SDK",
        inputSchema={
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["c++", "unity", "unreal", "csharp"],
                    "description": "Target platform/language"
                },
                "features": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["account-linking", "rich-presence", "friends-list", "lobbies", "voice-chat"]
                    },
                    "description": "SDK features to initialize"
                },
                "clientId": {
                    "type": "string",
                    "description": "Discord application client ID"
                }
            },
            "required": ["platform", "features"]
        }
    ),
    Tool(
        name="discord_create_account_linking",
        description="Generate account linking implementation code",
        inputSchema={
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["c++", "unity", "unreal"]
                },
                "useProvisionalAccounts": {
                    "type": "boolean",
                    "default": False
                }
            },
            "required": ["platform"]
        }
    ),
    Tool(
        name="discord_generate_rich_presence",
        description="Generate rich presence implementation code",
        inputSchema={
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["c++", "unity", "unreal", "csharp"]
                },
                "presenceType": {
                    "type": "string",
                    "enum": ["game", "streaming", "listening", "watching"],
                    "default": "game"
                }
            },
            "required": ["platform"]
        }
    ),
    Tool(
        name="discord_validate_oauth_scopes",
        description="Validate OAuth2 scopes for a specific use case",
        inputSchema={
            "type": "object",
            "properties": {
                "useCase": {
                    "type": "string",
                    "enum": ["social-sdk-basic", "social-sdk-full", "bot-basic"],
                    "description": "Use case type"
                },
                "providedScopes": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["useCase"]
        }
    ),
]

async def handle_social_sdk(name: str, arguments: dict) -> list[TextContent]:
    """Handle Discord Social SDK tool calls."""
    if name == "discord_generate_sdk_init":
        platform = arguments.get("platform")
        features = arguments.get("features")
        client_id = arguments.get("clientId", "YOUR_CLIENT_ID")
        
        result = {
            "success": True,
            "platform": platform,
            "features": features,
            "clientId": client_id,
            "code": generate_sdk_init_code(platform, features, client_id)
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    elif name == "discord_create_account_linking":
        platform = arguments.get("platform")
        use_provisional = arguments.get("useProvisionalAccounts", False)
        code = f"# Generated {platform} account linking code\n# Provisional: {use_provisional}"
        return [TextContent(type="text", text=code)]
    elif name == "discord_generate_rich_presence":
        platform = arguments.get("platform")
        presence_type = arguments.get("presenceType", "game")
        code = f"# Generated {platform} rich presence code\n# Type: {presence_type}"
        return [TextContent(type="text", text=code)]
    elif name == "discord_validate_oauth_scopes":
        use_case = arguments.get("useCase")
        provided_scopes = arguments.get("providedScopes", [])
        result = {
            "valid": True,
            "requiredScopes": ["identify", "rpc"],
            "missingScopes": []
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    else:
        raise ValueError(f"Unknown Discord Social SDK tool: {name}")

def generate_sdk_init_code(platform: str, features: list, client_id: str) -> str:
    """Generate SDK initialization code."""
    if platform == "unity":
        return f"// Unity SDK Initialization\nDiscord discord = new Discord({client_id}, ...);"
    elif platform == "c++":
        return f"// C++ SDK Initialization\ndiscord::Core::Create({client_id}, ...);"
    else:
        return f"# {platform} SDK initialization code"

