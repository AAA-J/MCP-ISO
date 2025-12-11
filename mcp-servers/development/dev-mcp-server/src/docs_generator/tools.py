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

def generate_markdown_docs(tools: list, resources: list, server_name: str) -> str:
    """Generate markdown API documentation."""
    doc = f"# {server_name} API Documentation\n\n"
    doc += f"## Overview\n\nThis MCP server provides {len(tools)} tools and {len(resources)} resources.\n\n"
    
    if tools:
        doc += "## Tools\n\n"
        for tool in tools:
            doc += f"### {tool.get('name', 'Unknown')}\n\n"
            doc += f"{tool.get('description', 'No description')}\n\n"
            
            input_schema = tool.get('inputSchema', {})
            properties = input_schema.get('properties', {})
            required = input_schema.get('required', [])
            
            if properties:
                doc += "**Parameters:**\n\n"
                for prop_name, prop_schema in properties.items():
                    prop_type = prop_schema.get('type', 'string')
                    prop_desc = prop_schema.get('description', '')
                    is_required = prop_name in required
                    doc += f"- `{prop_name}` ({prop_type}){' **required**' if is_required else ''}: {prop_desc}\n"
                doc += "\n"
    
    if resources:
        doc += "## Resources\n\n"
        for resource in resources:
            doc += f"### {resource.get('name', 'Unknown')}\n\n"
            doc += f"**URI:** `{resource.get('uri', '')}`\n\n"
            doc += f"{resource.get('description', 'No description')}\n\n"
    
    return doc

def generate_readme(server_config: dict, include_examples: bool = True) -> str:
    """Generate README.md from server configuration."""
    server_name = server_config.get("name", "MCP Server")
    description = server_config.get("description", "An MCP server")
    version = server_config.get("version", "0.1.0")
    language = server_config.get("language", "python")
    features = server_config.get("features", [])
    
    readme = f"# {server_name}\n\n"
    readme += f"{description}\n\n"
    readme += f"**Version:** {version}\n\n"
    
    if features:
        readme += "## Features\n\n"
        for feature in features:
            readme += f"- **{feature.capitalize()}**\n"
        readme += "\n"
    
    readme += "## Installation\n\n"
    if language == "python":
        readme += "```bash\n"
        readme += "python -m venv venv\n"
        readme += "source venv/bin/activate  # or venv\\Scripts\\activate on Windows\n"
        readme += "pip install -r requirements.txt\n"
        readme += "```\n\n"
    else:
        readme += "```bash\n"
        readme += "npm install\n"
        readme += "```\n\n"
    
    readme += "## Usage\n\n"
    if language == "python":
        readme += "```bash\n"
        readme += "python src/index.py\n"
        readme += "```\n\n"
    else:
        readme += "```bash\n"
        readme += "npm run dev\n"
        readme += "```\n\n"
    
    if include_examples:
        readme += "## Example\n\n"
        readme += "```json\n"
        readme += '{\n'
        readme += '  "mcpServers": {\n'
        readme += f'    "{server_name.lower()}": {{\n'
        if language == "python":
            readme += '      "command": "python",\n'
            readme += '      "args": ["src/index.py"]\n'
        else:
            readme += '      "command": "node",\n'
            readme += '      "args": ["dist/index.js"]\n'
        readme += '    }\n'
        readme += '  }\n'
        readme += '}\n'
        readme += "```\n\n"
    
    return readme

async def handle_docs_generator(name: str, arguments: dict) -> list[TextContent]:
    """Handle docs generator tool calls."""
    if name == "generate_api_docs":
        server_path = arguments.get("serverPath")
        output_format = arguments.get("outputFormat", "markdown")
        
        # In a real implementation, this would parse the server code
        # For now, generate a template
        tools = [
            {"name": "example_tool", "description": "Example tool", "inputSchema": {"properties": {}}}
        ]
        resources = [
            {"name": "Example Resource", "uri": "mcp://server/example", "description": "Example resource"}
        ]
        
        if output_format == "markdown":
            docs = generate_markdown_docs(tools, resources, "MCP Server")
        elif output_format == "json":
            docs = json.dumps({"tools": tools, "resources": resources}, indent=2)
        else:
            docs = f"# API Documentation\n\nGenerated from {server_path}\nFormat: {output_format}"
        
        return [TextContent(type="text", text=docs)]
    
    elif name == "generate_readme":
        server_config = arguments.get("serverConfig")
        include_examples = arguments.get("includeExamples", True)
        readme = generate_readme(server_config, include_examples)
        return [TextContent(type="text", text=readme)]
    
    else:
        raise ValueError(f"Unknown docs generator tool: {name}")

