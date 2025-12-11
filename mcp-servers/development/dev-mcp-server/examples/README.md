# Dev-MCP-Server Examples

This directory contains examples demonstrating how to use the Dev-MCP-Server.

## Examples

### basic_usage.py
Demonstrates basic usage patterns for:
- Scaffolding a new MCP server
- Generating tool handlers
- Validating tool schemas

## Usage

These examples show the expected tool call formats. In practice, you would call these tools through an MCP client (like Claude Desktop or another MCP-compatible client).

## Example Tool Calls

### Scaffold a Server
```json
{
  "tool": "scaffold_mcp_server",
  "arguments": {
    "serverName": "my-server",
    "language": "python",
    "features": ["tools", "resources"]
  }
}
```

### Generate Tool Handler
```json
{
  "tool": "generate_tool_handler",
  "arguments": {
    "toolSchema": {
      "name": "my_tool",
      "description": "Does something",
      "inputSchema": {
        "type": "object",
        "properties": {
          "input": {"type": "string"}
        },
        "required": ["input"]
      }
    },
    "language": "python"
  }
}
```

### Validate Schema
```json
{
  "tool": "validate_tool_schema",
  "arguments": {
    "toolSchema": {
      "name": "example",
      "description": "Example tool",
      "inputSchema": {
        "type": "object",
        "properties": {}
      }
    }
  }
}
```

## More Examples

See the main README.md for more comprehensive examples and usage patterns.

