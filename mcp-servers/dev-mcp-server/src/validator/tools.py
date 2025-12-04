"""Validation tools for MCP servers."""

from mcp.types import Tool, TextContent
import json
import os
from pathlib import Path
from typing import Dict, Any, List

validator_tools = [
    Tool(
        name="validate_server_structure",
        description="Validate MCP server project structure",
        inputSchema={
            "type": "object",
            "properties": {
                "projectPath": {
                    "type": "string",
                    "description": "Path to project directory"
                }
            },
            "required": ["projectPath"]
        }
    ),
    Tool(
        name="validate_tool_schema",
        description="Validate tool schema against MCP specification",
        inputSchema={
            "type": "object",
            "properties": {
                "toolSchema": {
                    "type": "object",
                    "description": "Tool schema to validate"
                },
                "strict": {
                    "type": "boolean",
                    "default": False
                }
            },
            "required": ["toolSchema"]
        }
    ),
    Tool(
        name="validate_jsonrpc",
        description="Validate JSON-RPC 2.0 compliance",
        inputSchema={
            "type": "object",
            "properties": {
                "message": {
                    "type": "object",
                    "description": "JSON-RPC message to validate"
                }
            },
            "required": ["message"]
        }
    ),
]

def validate_server_structure(project_path: str) -> Dict[str, Any]:
    """Validate MCP server project structure."""
    errors = []
    warnings = []
    path = Path(project_path)
    
    if not path.exists():
        return {
            "valid": False,
            "errors": [f"Project path does not exist: {project_path}"],
            "warnings": []
        }
    
    # Check for Python server
    python_files = list(path.rglob("*.py"))
    ts_files = list(path.rglob("*.ts"))
    
    if python_files:
        # Python server checks
        index_files = [f for f in python_files if "index.py" in str(f) or "server.py" in str(f) or "main.py" in str(f)]
        if not index_files:
            errors.append("No main entry point found (index.py, server.py, or main.py)")
        
        req_file = path / "requirements.txt"
        if not req_file.exists():
            warnings.append("No requirements.txt found")
        
        src_dir = path / "src"
        if not src_dir.exists():
            warnings.append("No src/ directory found")
    
    elif ts_files:
        # TypeScript server checks
        index_files = [f for f in ts_files if "index.ts" in str(f)]
        if not index_files:
            errors.append("No index.ts found")
        
        package_json = path / "package.json"
        if not package_json.exists():
            errors.append("No package.json found")
        
        tsconfig = path / "tsconfig.json"
        if not tsconfig.exists():
            warnings.append("No tsconfig.json found")
    
    else:
        warnings.append("No Python or TypeScript files found")
    
    # Check for .gitignore
    gitignore = path / ".gitignore"
    if not gitignore.exists():
        warnings.append("No .gitignore found")
    
    # Check for README
    readme = path / "README.md"
    if not readme.exists():
        warnings.append("No README.md found")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def validate_tool_schema(tool_schema: Dict[str, Any], strict: bool = False) -> Dict[str, Any]:
    """Validate tool schema against MCP specification."""
    errors = []
    warnings = []
    
    # Required fields
    if "name" not in tool_schema:
        errors.append("Tool schema missing required field: name")
    elif not isinstance(tool_schema["name"], str):
        errors.append("Tool name must be a string")
    elif not tool_schema["name"]:
        errors.append("Tool name cannot be empty")
    elif " " in tool_schema["name"]:
        warnings.append("Tool name contains spaces (consider using underscores)")
    
    if "description" not in tool_schema:
        errors.append("Tool schema missing required field: description")
    elif not isinstance(tool_schema["description"], str):
        errors.append("Tool description must be a string")
    elif len(tool_schema["description"]) < 10:
        warnings.append("Tool description is very short (consider adding more detail)")
    
    if "inputSchema" not in tool_schema:
        errors.append("Tool schema missing required field: inputSchema")
    else:
        input_schema = tool_schema["inputSchema"]
        
        if not isinstance(input_schema, dict):
            errors.append("inputSchema must be an object")
        else:
            if "type" not in input_schema:
                errors.append("inputSchema missing required field: type")
            elif input_schema["type"] != "object":
                errors.append("inputSchema type must be 'object'")
            
            if "properties" in input_schema:
                properties = input_schema["properties"]
                if not isinstance(properties, dict):
                    errors.append("inputSchema.properties must be an object")
                else:
                    required = input_schema.get("required", [])
                    for prop_name, prop_schema in properties.items():
                        if not isinstance(prop_schema, dict):
                            errors.append(f"Property '{prop_name}' schema must be an object")
                            continue
                        
                        if "type" not in prop_schema:
                            warnings.append(f"Property '{prop_name}' missing type")
                        
                        if "description" not in prop_schema:
                            warnings.append(f"Property '{prop_name}' missing description")
                        
                        if prop_name in required and prop_schema.get("type") == "string" and not prop_schema.get("description"):
                            warnings.append(f"Required property '{prop_name}' should have a description")
    
    if strict:
        # Additional strict validations
        if tool_schema.get("name") and not tool_schema["name"].islower():
            warnings.append("Tool name should be lowercase (convention)")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def validate_jsonrpc(message: Dict[str, Any]) -> Dict[str, Any]:
    """Validate JSON-RPC 2.0 compliance."""
    errors = []
    
    # Check JSON-RPC version
    if "jsonrpc" not in message:
        errors.append("Missing 'jsonrpc' field")
    elif message["jsonrpc"] != "2.0":
        errors.append(f"Invalid jsonrpc version: {message['jsonrpc']} (must be '2.0')")
    
    # Check for id (required for requests/responses, optional for notifications)
    if "id" not in message and "method" in message:
        # This is a notification, which is valid
        pass
    elif "id" in message:
        if not isinstance(message["id"], (str, int, type(None))):
            errors.append("'id' must be a string, number, or null")
    
    # Check for method (required for requests)
    if "method" in message:
        if not isinstance(message["method"], str):
            errors.append("'method' must be a string")
        if not message["method"]:
            errors.append("'method' cannot be empty")
    
    # Check for result or error (required for responses)
    if "result" in message and "error" in message:
        errors.append("Response cannot have both 'result' and 'error'")
    
    if "error" in message:
        error = message["error"]
        if not isinstance(error, dict):
            errors.append("'error' must be an object")
        else:
            if "code" not in error:
                errors.append("Error object missing 'code'")
            elif not isinstance(error["code"], int):
                errors.append("Error 'code' must be an integer")
            
            if "message" not in error:
                errors.append("Error object missing 'message'")
            elif not isinstance(error["message"], str):
                errors.append("Error 'message' must be a string")
    
    # Check for params (optional)
    if "params" in message:
        if not isinstance(message["params"], (dict, list)):
            errors.append("'params' must be an object or array")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

async def handle_validator(name: str, arguments: dict) -> list[TextContent]:
    """Handle validator tool calls."""
    if name == "validate_server_structure":
        project_path = arguments.get("projectPath")
        result = validate_server_structure(project_path)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "validate_tool_schema":
        tool_schema = arguments.get("toolSchema")
        strict = arguments.get("strict", False)
        result = validate_tool_schema(tool_schema, strict)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "validate_jsonrpc":
        message = arguments.get("message")
        result = validate_jsonrpc(message)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    else:
        raise ValueError(f"Unknown validator tool: {name}")

