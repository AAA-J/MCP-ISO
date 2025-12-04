"""Testing tools for MCP servers."""

from mcp.types import Tool, TextContent
import json

tester_tools = [
    Tool(
        name="test_tool_call",
        description="Test a tool call with mock data",
        inputSchema={
            "type": "object",
            "properties": {
                "toolName": {
                    "type": "string"
                },
                "arguments": {
                    "type": "object"
                },
                "serverPath": {
                    "type": "string",
                    "description": "Path to MCP server executable"
                }
            },
            "required": ["toolName", "arguments"]
        }
    ),
    Tool(
        name="test_resource_read",
        description="Test resource reading",
        inputSchema={
            "type": "object",
            "properties": {
                "resourceUri": {
                    "type": "string"
                },
                "serverPath": {
                    "type": "string"
                }
            },
            "required": ["resourceUri"]
        }
    ),
    Tool(
        name="generate_test_cases",
        description="Generate test cases from tool schemas",
        inputSchema={
            "type": "object",
            "properties": {
                "toolSchemas": {
                    "type": "array",
                    "items": {"type": "object"}
                },
                "language": {
                    "type": "string",
                    "enum": ["python", "typescript"]
                }
            },
            "required": ["toolSchemas", "language"]
        }
    ),
]

def generate_python_test_cases(tool_schemas: list) -> str:
    """Generate Python test cases from tool schemas."""
    test_code = '''"""Generated test cases for MCP server tools."""
import pytest
from mcp.types import TextContent

'''
    
    for schema in tool_schemas:
        tool_name = schema.get("name", "unknown_tool")
        input_schema = schema.get("inputSchema", {})
        properties = input_schema.get("properties", {})
        required = input_schema.get("required", [])
        
        # Generate test function
        test_func = f'''@pytest.mark.asyncio
async def test_{tool_name}():
    """Test {tool_name} tool."""
    # Test with valid input
    arguments = {{'''
        
        # Add test arguments
        for prop_name, prop_schema in properties.items():
            prop_type = prop_schema.get("type", "string")
            if prop_type == "string":
                test_value = f'"{prop_name}_value"'
            elif prop_type == "integer":
                test_value = "42"
            elif prop_type == "number":
                test_value = "3.14"
            elif prop_type == "boolean":
                test_value = "True"
            elif prop_type == "array":
                test_value = '["item1", "item2"]'
            else:
                test_value = '{"key": "value"}'
            
            test_func += f'\n        "{prop_name}": {test_value},'
        
        test_func += '''
    }
    
    # Call handler (replace with actual handler import)
    # result = await handle_{tool_name}(arguments)
    # assert isinstance(result, list)
    # assert len(result) > 0
    # assert isinstance(result[0], TextContent)

'''
        
        # Add validation test
        if required:
            test_func += f'''@pytest.mark.asyncio
async def test_{tool_name}_validation():
    """Test {tool_name} validation."""
    # Test missing required parameter
    arguments = {{}}
    # Should raise ValueError
    # with pytest.raises(ValueError):
    #     await handle_{tool_name}(arguments)

'''
        
        test_code += test_func
    
    return test_code

def generate_typescript_test_cases(tool_schemas: list) -> str:
    """Generate TypeScript test cases from tool schemas."""
    test_code = '''/**
 * Generated test cases for MCP server tools
 */
import { describe, it, expect } from "@jest/globals";

'''
    
    for schema in tool_schemas:
        tool_name = schema.get("name", "unknownTool")
        input_schema = schema.get("inputSchema", {})
        properties = input_schema.get("properties", {})
        required = input_schema.get("required", [])
        
        test_code += f'''describe("{tool_name}", () => {{
  it("should handle valid input", async () => {{
    const arguments = {{'''
        
        for prop_name, prop_schema in properties.items():
            prop_type = prop_schema.get("type", "string")
            if prop_type == "string":
                test_value = f'"{prop_name}_value"'
            elif prop_type == "integer" or prop_type == "number":
                test_value = "42"
            elif prop_type == "boolean":
                test_value = "true"
            elif prop_type == "array":
                test_value = '["item1", "item2"]'
            else:
                test_value = '{ key: "value" }'
            
            test_code += f'\n      {prop_name}: {test_value},'
        
        test_code += '''
    };
    
    // Call handler (replace with actual handler import)
    // const result = await handle' + tool_name.charAt(0).upper() + tool_name.slice(1) + '(arguments);
    // expect(result).toBeInstanceOf(Array);
    // expect(result.length).toBeGreaterThan(0);
  });
'''
        
        if required:
            test_code += f'''
  it("should validate required parameters", async () => {{
    const arguments = {{}};
    // Should throw error
    // await expect(handle' + tool_name.charAt(0).upper() + tool_name.slice(1) + '(arguments)).rejects.toThrow();
  }});
'''
        
        test_code += '});\n\n'
    
    return test_code

async def handle_tester(name: str, arguments: dict) -> list[TextContent]:
    """Handle tester tool calls."""
    if name == "test_tool_call":
        tool_name = arguments.get("toolName")
        test_args = arguments.get("arguments")
        server_path = arguments.get("serverPath")
        
        # In a real implementation, this would actually execute the tool
        result = {
            "success": True,
            "tool": tool_name,
            "arguments": test_args,
            "response": "Mock response (implementation would execute actual tool)",
            "duration": "0.1s",
            "note": f"To actually test, provide serverPath: {server_path or 'not provided'}"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "test_resource_read":
        resource_uri = arguments.get("resourceUri")
        server_path = arguments.get("serverPath")
        
        result = {
            "success": True,
            "uri": resource_uri,
            "content": "Mock resource content (implementation would read actual resource)",
            "note": f"To actually test, provide serverPath: {server_path or 'not provided'}"
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "generate_test_cases":
        tool_schemas = arguments.get("toolSchemas")
        language = arguments.get("language")
        
        if language == "python":
            test_cases = generate_python_test_cases(tool_schemas)
        elif language == "typescript":
            test_cases = generate_typescript_test_cases(tool_schemas)
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        return [TextContent(type="text", text=test_cases)]
    
    else:
        raise ValueError(f"Unknown tester tool: {name}")

