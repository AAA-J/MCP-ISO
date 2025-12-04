"""Code generation tools for MCP servers."""

from mcp.types import Tool, TextContent
import json
from typing import Dict, Any

code_generator_tools = [
    Tool(
        name="generate_tool_handler",
        description="Generate tool handler code from tool schema",
        inputSchema={
            "type": "object",
            "properties": {
                "toolSchema": {
                    "type": "object",
                    "description": "Tool schema definition"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                },
                "framework": {
                    "type": "string",
                    "description": "MCP framework (mcp, @modelcontextprotocol/sdk)"
                }
            },
            "required": ["toolSchema", "language"]
        }
    ),
    Tool(
        name="generate_resource_handler",
        description="Generate resource handler code",
        inputSchema={
            "type": "object",
            "properties": {
                "resourceUri": {
                    "type": "string"
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                }
            },
            "required": ["resourceUri", "language"]
        }
    ),
    Tool(
        name="generate_type_definitions",
        description="Generate TypeScript or Python type definitions from schemas",
        inputSchema={
            "type": "object",
            "properties": {
                "schemas": {
                    "type": "array",
                    "items": {"type": "object"}
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                }
            },
            "required": ["schemas", "language"]
        }
    ),
]

def generate_python_tool_handler(tool_schema: Dict[str, Any]) -> str:
    """Generate Python tool handler code."""
    tool_name = tool_schema.get("name", "my_tool")
    description = tool_schema.get("description", "")
    input_schema = tool_schema.get("inputSchema", {})
    properties = input_schema.get("properties", {})
    required = input_schema.get("required", [])
    
    # Generate parameter extraction code
    param_extractions = []
    validations = []
    
    for param_name, param_schema in properties.items():
        param_type = param_schema.get("type", "string")
        param_desc = param_schema.get("description", "")
        is_required = param_name in required
        
        if is_required:
            validations.append(f'    if "{param_name}" not in arguments:\n        raise ValueError("{param_name} is required")')
        
        # Type conversion
        if param_type == "integer":
            param_extractions.append(f'    {param_name} = arguments.get("{param_name}")')
            if is_required:
                validations.append(f'    if not isinstance({param_name}, int):\n        raise ValueError("{param_name} must be an integer")')
        elif param_type == "number":
            param_extractions.append(f'    {param_name} = arguments.get("{param_name}")')
            if is_required:
                validations.append(f'    if not isinstance({param_name}, (int, float)):\n        raise ValueError("{param_name} must be a number")')
        elif param_type == "boolean":
            param_extractions.append(f'    {param_name} = arguments.get("{param_name}")')
        elif param_type == "array":
            param_extractions.append(f'    {param_name} = arguments.get("{param_name}", [])')
            if is_required:
                validations.append(f'    if not isinstance({param_name}, list):\n        raise ValueError("{param_name} must be an array")')
        else:
            param_extractions.append(f'    {param_name} = arguments.get("{param_name}")')
            if is_required:
                validations.append(f'    if not isinstance({param_name}, str):\n        raise ValueError("{param_name} must be a string")')
    
    code = f'''"""Tool handler for {tool_name}"""
from mcp.types import TextContent

async def handle_{tool_name}(arguments: dict) -> list[TextContent]:
    """
    Handle {tool_name} tool call.
    
    Description: {description}
    """
{chr(10).join(validations)}
{chr(10).join(param_extractions)}
    
    # TODO: Implement your tool logic here
    # Example:
    # result = process_data({", ".join(properties.keys())})
    
    result = "Tool executed successfully"
    
    return [TextContent(
        type="text",
        text=result
    )]
'''
    return code

def generate_typescript_tool_handler(tool_schema: Dict[str, Any]) -> str:
    """Generate TypeScript tool handler code."""
    tool_name = tool_schema.get("name", "myTool")
    description = tool_schema.get("description", "")
    input_schema = tool_schema.get("inputSchema", {})
    properties = input_schema.get("properties", {})
    required = input_schema.get("required", [])
    
    # Generate TypeScript interface
    interface_props = []
    for param_name, param_schema in properties.items():
        param_type = param_schema.get("type", "string")
        ts_type = {
            "string": "string",
            "integer": "number",
            "number": "number",
            "boolean": "boolean",
            "array": "any[]",
            "object": "Record<string, any>"
        }.get(param_type, "any")
        
        optional = "" if param_name in required else "?"
        interface_props.append(f"  {param_name}{optional}: {ts_type};")
    
    interface_code = f"interface {tool_name.capitalize()}Arguments {{\n" + "\n".join(interface_props) + "\n}"
    
    code = f'''/**
 * Tool handler for {tool_name}
 * 
 * Description: {description}
 */
import {{ TextContent }} from "@modelcontextprotocol/sdk/types.js";

{interface_code}

export async function handle{tool_name.charAt(0).upper() + tool_name.slice(1)}(
  arguments: {tool_name.capitalize()}Arguments
): Promise<TextContent[]> {{
  // TODO: Implement your tool logic here
  // Example:
  // const result = processData(arguments);
  
  const result = "Tool executed successfully";
  
  return [
    {{
      type: "text",
      text: result,
    }},
  ];
}}
'''
    return code

def generate_python_resource_handler(resource_uri: str) -> str:
    """Generate Python resource handler code."""
    uri_parts = resource_uri.replace("mcp://", "").split("/")
    resource_name = "_".join(uri_parts[-2:]) if len(uri_parts) > 1 else uri_parts[-1]
    
    code = f'''"""Resource handler for {resource_uri}"""
from mcp.types import TextContent

async def read_{resource_name}(uri: str) -> str:
    """
    Read resource from URI: {resource_uri}
    
    Args:
        uri: Resource URI to read
        
    Returns:
        Resource content as string
    """
    # Validate URI
    if not uri.startswith("{resource_uri.split("://")[0]}://"):
        raise ValueError(f"Invalid URI: {{uri}}")
    
    # Extract resource identifier from URI
    # Example: resource_id = uri.split("/")[-1]
    
    # TODO: Implement resource reading logic
    # Example:
    # with open(file_path, "r") as f:
    #     return f.read()
    
    return "Resource content"
'''
    return code

def generate_typescript_resource_handler(resource_uri: str) -> str:
    """Generate TypeScript resource handler code."""
    uri_parts = resource_uri.replace("mcp://", "").split("/")
    resource_name = uri_parts[-1] if uri_parts else "resource"
    
    code = f'''/**
 * Resource handler for {resource_uri}
 */
export async function read{resource_name.charAt(0).upper() + resource_name.slice(1)}(
  uri: string
): Promise<string> {{
  // Validate URI
  if (!uri.startsWith("{resource_uri.split("://")[0]}://")) {{
    throw new Error(`Invalid URI: ${{uri}}`);
  }}
  
  // Extract resource identifier from URI
  // Example: const resourceId = uri.split("/").pop();
  
  // TODO: Implement resource reading logic
  // Example:
  // const fs = await import("fs/promises");
  // return await fs.readFile(filePath, "utf-8");
  
  return "Resource content";
}}
'''
    return code

def generate_python_types(schemas: list) -> str:
    """Generate Python type definitions."""
    type_defs = []
    
    for schema in schemas:
        schema_name = schema.get("name", "Schema")
        properties = schema.get("properties", {})
        
        type_def = f'''class {schema_name}:
    """Type definition for {schema_name}"""
    
    def __init__(self'''
        
        params = []
        for prop_name, prop_schema in properties.items():
            prop_type = prop_schema.get("type", "str")
            python_type = {
                "string": "str",
                "integer": "int",
                "number": "float",
                "boolean": "bool",
                "array": "list",
                "object": "dict"
            }.get(prop_type, "Any")
            
            default = "None" if prop_name not in schema.get("required", []) else ""
            params.append(f"{prop_name}: {python_type}{' = ' + default if default else ''}")
        
        type_def += ", " + ", ".join(params) + "):\n"
        
        for prop_name in properties.keys():
            type_def += f"        self.{prop_name} = {prop_name}\n"
        
        type_defs.append(type_def)
    
    return "\n".join(type_defs)

def generate_typescript_types(schemas: list) -> str:
    """Generate TypeScript type definitions."""
    type_defs = []
    
    for schema in schemas:
        schema_name = schema.get("name", "Schema")
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        type_def = f"export interface {schema_name} {{\n"
        
        for prop_name, prop_schema in properties.items():
            prop_type = prop_schema.get("type", "string")
            ts_type = {
                "string": "string",
                "integer": "number",
                "number": "number",
                "boolean": "boolean",
                "array": "any[]",
                "object": "Record<string, any>"
            }.get(prop_type, "any")
            
            optional = "" if prop_name in required else "?"
            type_def += f"  {prop_name}{optional}: {ts_type};\n"
        
        type_def += "}"
        type_defs.append(type_def)
    
    return "\n\n".join(type_defs)

async def handle_code_generator(name: str, arguments: dict) -> list[TextContent]:
    """Handle code generator tool calls."""
    if name == "generate_tool_handler":
        tool_schema = arguments.get("toolSchema")
        language = arguments.get("language")
        
        if language == "python":
            code = generate_python_tool_handler(tool_schema)
        elif language == "typescript":
            code = generate_typescript_tool_handler(tool_schema)
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        return [TextContent(type="text", text=code)]
    
    elif name == "generate_resource_handler":
        resource_uri = arguments.get("resourceUri")
        language = arguments.get("language")
        
        if language == "python":
            code = generate_python_resource_handler(resource_uri)
        elif language == "typescript":
            code = generate_typescript_resource_handler(resource_uri)
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        return [TextContent(type="text", text=code)]
    
    elif name == "generate_type_definitions":
        schemas = arguments.get("schemas")
        language = arguments.get("language")
        
        if language == "python":
            code = generate_python_types(schemas)
        elif language == "typescript":
            code = generate_typescript_types(schemas)
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        return [TextContent(type="text", text=code)]
    
    else:
        raise ValueError(f"Unknown code generator tool: {name}")

