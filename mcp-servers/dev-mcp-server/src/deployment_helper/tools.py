"""Deployment helper tools for MCP servers."""

from mcp.types import Tool, TextContent
import json

deployment_helper_tools = [
    Tool(
        name="generate_dockerfile",
        description="Generate Dockerfile for MCP server deployment",
        inputSchema={
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript", "node"]
                },
                "baseImage": {
                    "type": "string",
                    "description": "Base Docker image"
                },
                "serverPath": {
                    "type": "string",
                    "description": "Path to server entry point"
                }
            },
            "required": ["language"]
        }
    ),
    Tool(
        name="validate_deployment",
        description="Validate deployment configuration",
        inputSchema={
            "type": "object",
            "properties": {
                "config": {
                    "type": "object",
                    "description": "Deployment configuration"
                }
            },
            "required": ["config"]
        }
    ),
]

def generate_python_dockerfile(base_image: str, server_path: str) -> str:
    """Generate Dockerfile for Python MCP server."""
    dockerfile = f'''# Dockerfile for Python MCP Server
FROM {base_image or "python:3.11-slim"}

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Run the server
CMD ["python", "{server_path or 'src/index.py'}"]
'''
    return dockerfile

def generate_typescript_dockerfile(base_image: str, server_path: str) -> str:
    """Generate Dockerfile for TypeScript MCP server."""
    dockerfile = f'''# Dockerfile for TypeScript MCP Server
FROM {base_image or "node:20-slim"}

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build TypeScript
RUN npm run build

# Run the server
CMD ["node", "{server_path or 'dist/index.js'}"]
'''
    return dockerfile

def validate_deployment_config(config: dict) -> dict:
    """Validate deployment configuration."""
    errors = []
    warnings = []
    
    # Check required fields
    if "language" not in config:
        errors.append("Missing required field: language")
    
    if "serverPath" not in config:
        warnings.append("Missing serverPath (using default)")
    
    # Validate language-specific configs
    language = config.get("language")
    if language == "python":
        if "requirementsFile" not in config:
            warnings.append("No requirementsFile specified")
    elif language == "typescript":
        if "buildCommand" not in config:
            warnings.append("No buildCommand specified")
    
    # Check Docker config
    if "docker" in config:
        docker_config = config["docker"]
        if "baseImage" not in docker_config:
            warnings.append("No Docker baseImage specified (using default)")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

async def handle_deployment_helper(name: str, arguments: dict) -> list[TextContent]:
    """Handle deployment helper tool calls."""
    if name == "generate_dockerfile":
        language = arguments.get("language")
        base_image = arguments.get("baseImage")
        server_path = arguments.get("serverPath")
        
        if language == "python":
            dockerfile = generate_python_dockerfile(base_image, server_path)
        elif language == "typescript" or language == "node":
            dockerfile = generate_typescript_dockerfile(base_image, server_path)
        else:
            raise ValueError(f"Unsupported language for Dockerfile: {language}")
        
        return [TextContent(type="text", text=dockerfile)]
    
    elif name == "validate_deployment":
        config = arguments.get("config")
        result = validate_deployment_config(config)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    else:
        raise ValueError(f"Unknown deployment helper tool: {name}")

