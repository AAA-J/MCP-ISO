# Dev-MCP-Server

A Model Context Protocol (MCP) server that helps developers build MCP servers. This server provides tools for scaffolding, code generation, validation, testing, and deployment of MCP servers.

## Features

- **Spec Reference** - Access MCP specification and best practices
- **Scaffolder** - Generate starter project structures
- **Code Generator** - Generate tool handlers, resources, and prompts
- **Tester** - Test MCP servers without manual setup
- **Example Library** - Reference implementations and patterns
- **Validator** - Validate MCP server compliance
- **Docs Generator** - Generate documentation from code
- **Deployment Helper** - Prepare MCP servers for deployment
- **Package Manager** - Manage dependencies and versions

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the MCP server:

```bash
python src/index.py
```

Configure in your MCP client:

```json
{
  "mcpServers": {
    "dev-mcp-server": {
      "command": "python",
      "args": ["/path/to/mcp-servers/dev-mcp-server/src/index.py"]
    }
  }
}
```

## Available Tools

### Spec Reference
- `get_mcp_spec` - Get MCP specification details
- `get_best_practices` - Get best practices for patterns

### Scaffolder
- `scaffold_mcp_server` - Generate new MCP server project
- `add_tool_template` - Add tool boilerplate
- `add_resource_template` - Add resource boilerplate

### Code Generator
- `generate_tool_handler` - Generate tool handler code
- `generate_resource_handler` - Generate resource handler code
- `generate_type_definitions` - Generate TypeScript/Python types

### Validator
- `validate_server_structure` - Validate project structure
- `validate_tool_schema` - Validate tool schemas
- `validate_jsonrpc` - Validate JSON-RPC compliance

### Tester
- `test_tool_call` - Test tool calls
- `test_resource_read` - Test resource reading
- `generate_test_cases` - Generate test cases

### Example Library
- `get_example_server` - Get example server code
- `get_pattern` - Get common patterns

### Docs Generator
- `generate_api_docs` - Generate API documentation
- `generate_readme` - Generate README from config

### Deployment Helper
- `generate_dockerfile` - Generate Dockerfile
- `validate_deployment` - Validate deployment config

### Package Manager
- `check_dependencies` - Check dependency versions
- `suggest_dependencies` - Suggest dependencies

## Examples

See the `examples/` directory for usage examples.

## Documentation

For general MCP development documentation, see:
- [MCP Server Guide](../../docs/MCP_SERVER_GUIDE.md)
- [MCP Best Use Cases](../../docs/MCP_BEST_USE_CASES.md)

