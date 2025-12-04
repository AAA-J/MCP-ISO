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
        tool_name = arguments.get("toolName")
        description = arguments.get("description")
        language = arguments.get("language")
        output_path = arguments.get("outputPath", ".")
        
        if language == "python":
            tool_code = f'''"""Tool: {tool_name}"""
from mcp.types import Tool, TextContent

{tool_name}_tool = Tool(
    name="{tool_name}",
    description="{description}",
    inputSchema={{
        "type": "object",
        "properties": {{
            "input": {{
                "type": "string",
                "description": "Input parameter"
            }}
        }},
        "required": ["input"]
    }}
)

async def handle_{tool_name}(arguments: dict) -> list[TextContent]:
    """Handle {tool_name} tool call."""
    input_value = arguments.get("input")
    
    # TODO: Implement your tool logic
    result = f"Processed: {{input_value}}"
    
    return [TextContent(type="text", text=result)]
'''
        else:  # TypeScript
            tool_code = f'''/**
 * Tool: {tool_name}
 * Description: {description}
 */
import {{ Tool }} from "@modelcontextprotocol/sdk/types.js";
import {{ TextContent }} from "@modelcontextprotocol/sdk/types.js";

export const {tool_name}Tool: Tool = {{
  name: "{tool_name}",
  description: "{description}",
  inputSchema: {{
    type: "object",
    properties: {{
      input: {{
        type: "string",
        description: "Input parameter",
      }},
    }},
    required: ["input"],
  }},
}};

export async function handle{tool_name.charAt(0).upper() + tool_name.slice(1)}(
  arguments: {{ input: string }}
): Promise<TextContent[]> {{
  // TODO: Implement your tool logic
  const result = `Processed: ${{arguments.input}}`;
  
  return [
    {{
      type: "text",
      text: result,
    }},
  ];
}}
'''
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "tool": tool_name,
                "language": language,
                "code": tool_code,
                "outputPath": output_path,
                "filename": f"{tool_name}.{'py' if language == 'python' else 'ts'}"
            }, indent=2)
        )]
    
    elif name == "add_resource_template":
        resource_uri = arguments.get("resourceUri")
        resource_name = arguments.get("resourceName")
        language = arguments.get("language")
        output_path = arguments.get("outputPath", ".")
        
        if language == "python":
            resource_code = f'''"""Resource: {resource_name}"""
from mcp.types import Resource

{resource_name.lower().replace("-", "_")}_resource = Resource(
    uri="{resource_uri}",
    name="{resource_name}",
    description="Resource description",
    mimeType="text/plain"
)

async def read_{resource_name.lower().replace("-", "_")}(uri: str) -> str:
    """Read {resource_name} resource."""
    # Validate URI
    if not uri.startswith("{resource_uri.split("://")[0]}://"):
        raise ValueError(f"Invalid URI: {{uri}}")
    
    # TODO: Implement resource reading logic
    return "Resource content"
'''
        else:  # TypeScript
            resource_code = f'''/**
 * Resource: {resource_name}
 * URI: {resource_uri}
 */
import {{ Resource }} from "@modelcontextprotocol/sdk/types.js";

export const {resource_name.replace("-", "")}Resource: Resource = {{
  uri: "{resource_uri}",
  name: "{resource_name}",
  description: "Resource description",
  mimeType: "text/plain",
}};

export async function read{resource_name.replace("-", "")}(
  uri: string
): Promise<string> {{
  // Validate URI
  if (!uri.startsWith("{resource_uri.split("://")[0]}://")) {{
    throw new Error(`Invalid URI: ${{uri}}`);
  }}
  
  // TODO: Implement resource reading logic
  return "Resource content";
}}
'''
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "resource": resource_name,
                "uri": resource_uri,
                "language": language,
                "code": resource_code,
                "outputPath": output_path,
                "filename": f"{resource_name.lower().replace(' ', '_')}.{'py' if language == 'python' else 'ts'}"
            }, indent=2)
        )]
    else:
        raise ValueError(f"Unknown scaffolder tool: {name}")

def generate_project_files(server_name: str, language: str, transport: str, features: list) -> dict:
    """Generate project file structure."""
    files = {}
    safe_name = server_name.lower().replace("-", "_").replace(" ", "_")
    
    if language == "python":
        # Main entry point
        files["src/index.py"] = f'''#!/usr/bin/env python3
"""
{safe_name} - MCP Server
"""

import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent

# Initialize MCP server
server = Server("{safe_name}")

# Import handlers
{"from tools.handlers import tool_handlers" if "tools" in features else ""}
{"from resources.handlers import resource_handlers" if "resources" in features else ""}

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return tool_handlers if "tools" in features else []

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    {"# Route to appropriate handler" if "tools" in features else "# No tools implemented"}
    raise ValueError(f"Unknown tool: {{name}}")

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return resource_handlers if "resources" in features else []

@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource."""
    {"# Route to appropriate handler" if "resources" in features else "# No resources implemented"}
    raise ValueError(f"Unknown resource: {{uri}}")

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
'''
        
        # Requirements file
        files["requirements.txt"] = f'''# {safe_name} Requirements
# MCP server for {server_name}

# Core MCP SDK
mcp>=0.1.0

# Standard library dependencies
python-dotenv>=1.0.0
'''
        
        # README
        files["README.md"] = f'''# {server_name}

MCP Server description

## Installation

```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```

## Usage

```bash
python src/index.py
```

## Features

{chr(10).join([f"- **{feature.capitalize()}**" for feature in features])}
'''
        
        # .gitignore
        files[".gitignore"] = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Distribution
dist/
build/
*.egg-info/
'''
        
        # Tools module
        if "tools" in features:
            files["src/tools/__init__.py"] = '''"""Tools module for MCP server."""
from .handlers import tool_handlers, handle_tool_call

__all__ = ["tool_handlers", "handle_tool_call"]
'''
            files["src/tools/handlers.py"] = '''"""Tool handlers."""
from mcp.types import Tool, TextContent

# Define tools
tool_handlers = [
    Tool(
        name="example_tool",
        description="Example tool",
        inputSchema={
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Input parameter"
                }
            },
            "required": ["input"]
        }
    ),
]

async def handle_tool_call(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "example_tool":
        input_value = arguments.get("input")
        return [TextContent(
            type="text",
            text=f"Processed: {input_value}"
        )]
    else:
        raise ValueError(f"Unknown tool: {name}")
'''
        
        # Resources module
        if "resources" in features:
            files["src/resources/__init__.py"] = '''"""Resources module for MCP server."""
from .handlers import resource_handlers, handle_resource_read

__all__ = ["resource_handlers", "handle_resource_read"]
'''
            files["src/resources/handlers.py"] = f'''"""Resource handlers."""
from mcp.types import Resource

# Define resources
resource_handlers = [
    Resource(
        uri="mcp://{safe_name}/example",
        name="Example Resource",
        description="Example resource",
        mimeType="text/plain"
    ),
]

async def handle_resource_read(uri: str) -> str:
    """Handle resource reading."""
    if uri.startswith("mcp://{safe_name}/example"):
        return "Example resource content"
    else:
        raise ValueError(f"Unknown resource: {{uri}}")
'''
        
        # Prompts module
        if "prompts" in features:
            files["src/prompts/__init__.py"] = '''"""Prompts module for MCP server."""
'''
    
    elif language == "typescript":
        # TypeScript implementation
        files["src/index.ts"] = f'''/**
 * {safe_name} - MCP Server
 */

import {{ Server }} from "@modelcontextprotocol/sdk/server/index.js";
import {{ StdioServerTransport }} from "@modelcontextprotocol/sdk/server/stdio.js";
import {{
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
}} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {{
    name: "{safe_name}",
    version: "0.1.0",
  }},
  {{
    capabilities: {{
      tools: {{}},
      resources: {{}},
    }},
  }}
);

{"// Register tools" if "tools" in features else ""}
{"server.setRequestHandler(ListToolsRequestSchema, async () => ({{ tools: [] }}));" if "tools" in features else ""}
{"server.setRequestHandler(CallToolRequestSchema, async (request) => {{ throw new Error('Not implemented'); }});" if "tools" in features else ""}

{"// Register resources" if "resources" in features else ""}
{"server.setRequestHandler(ListResourcesRequestSchema, async () => ({{ resources: [] }}));" if "resources" in features else ""}
{"server.setRequestHandler(ReadResourceRequestSchema, async (request) => {{ throw new Error('Not implemented'); }});" if "resources" in features else ""}

async function main() {{
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("{safe_name} server running on stdio");
}}

main().catch(console.error);
'''
        
        files["package.json"] = f'''{{
  "name": "{safe_name}",
  "version": "0.1.0",
  "description": "MCP Server for {server_name}",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {{
    "build": "tsc",
    "dev": "tsx src/index.ts"
  }},
  "dependencies": {{
    "@modelcontextprotocol/sdk": "^0.5.0"
  }},
  "devDependencies": {{
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0"
  }}
}}
'''
        
        files["tsconfig.json"] = '''{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
'''
    
    return files

