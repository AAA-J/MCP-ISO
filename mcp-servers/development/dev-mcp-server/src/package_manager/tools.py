"""Package management tools for MCP servers."""

from mcp.types import Tool, TextContent
import json

package_manager_tools = [
    Tool(
        name="check_dependencies",
        description="Check if dependencies are up to date",
        inputSchema={
            "type": "object",
            "properties": {
                "packageFile": {
                    "type": "string",
                    "description": "Path to package file (requirements.txt, package.json)"
                }
            },
            "required": ["packageFile"]
        }
    ),
    Tool(
        name="suggest_dependencies",
        description="Suggest dependencies based on MCP server features",
        inputSchema={
            "type": "object",
            "properties": {
                "features": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Server features (tools, resources, prompts, auth)"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                }
            },
            "required": ["features", "language"]
        }
    ),
]

def suggest_dependencies_for_features(features: list, language: str) -> dict:
    """Suggest dependencies based on features."""
    base_deps = {
        "python": ["mcp>=0.1.0", "python-dotenv>=1.0.0"],
        "typescript": ["@modelcontextprotocol/sdk>=0.5.0"]
    }
    
    feature_deps = {
        "python": {
            "http": ["httpx>=0.24.0", "fastapi>=0.100.0"],
            "database": ["sqlalchemy>=2.0.0"],
            "auth": ["python-jose>=3.3.0", "passlib>=1.7.4"],
            "async": ["aiohttp>=3.8.0"],
            "testing": ["pytest>=7.4.0", "pytest-asyncio>=0.21.0"]
        },
        "typescript": {
            "http": ["express>=4.18.0", "@types/express>=4.17.0"],
            "database": ["prisma>=5.0.0"],
            "auth": ["jsonwebtoken>=9.0.0", "@types/jsonwebtoken>=9.0.0"],
            "async": ["axios>=1.4.0"],
            "testing": ["jest>=29.0.0", "@types/jest>=29.0.0"]
        }
    }
    
    dependencies = base_deps.get(language, [])
    
    # Map features to dependency categories
    feature_map = {
        "tools": [],
        "resources": [],
        "prompts": [],
        "http": ["http"],
        "database": ["database"],
        "auth": ["auth"],
        "async": ["async"]
    }
    
    for feature in features:
        if feature in feature_map:
            deps = feature_deps.get(language, {}).get(feature, [])
            dependencies.extend(deps)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_deps = []
    for dep in dependencies:
        dep_name = dep.split(">=")[0].split("==")[0].split("@")[-1]
        if dep_name not in seen:
            seen.add(dep_name)
            unique_deps.append(dep)
    
    return {
        "language": language,
        "features": features,
        "dependencies": unique_deps,
        "devDependencies": feature_deps.get(language, {}).get("testing", []) if "testing" in features else []
    }

async def handle_package_manager(name: str, arguments: dict) -> list[TextContent]:
    """Handle package manager tool calls."""
    if name == "check_dependencies":
        package_file = arguments.get("packageFile")
        
        # In a real implementation, this would parse the package file
        # and check against package registries
        result = {
            "upToDate": True,
            "outdated": [],
            "latest": [],
            "message": f"Dependency check for {package_file} (implementation would check actual versions)"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "suggest_dependencies":
        features = arguments.get("features")
        language = arguments.get("language")
        suggestions = suggest_dependencies_for_features(features, language)
        return [TextContent(type="text", text=json.dumps(suggestions, indent=2))]
    
    else:
        raise ValueError(f"Unknown package manager tool: {name}")

