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

## Prerequisites

- Python 3.10+
- Basic understanding of MCP (Model Context Protocol)

## Installation

See **[SETUP.md](../../SETUP.md)** for detailed setup instructions.

**Quick setup**:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Or use the automated setup script from repository root: `./setup.sh`

## Usage

### Running the Server

```bash
# If using venv, make sure it's activated first
python src/index.py
```

### Configuring in MCP Client

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "dev-mcp-server": {
      "command": "python",
      "args": ["/path/to/mcp-servers/development/dev-mcp-server/src/index.py"]
    }
  }
}
```

If using venv, use the venv Python:

```json
{
  "mcpServers": {
    "dev-mcp-server": {
      "command": "/path/to/mcp-servers/development/dev-mcp-server/venv/bin/python",
      "args": ["/path/to/mcp-servers/development/dev-mcp-server/src/index.py"]
    }
  }
}
```

## Available Tools

### Spec Reference
- `spec_get_mcp_spec` - Get MCP specification details for a topic
- `spec_get_best_practices` - Get best practices for patterns

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
- `test_tool_call` - Test tool calls with mock data
- `test_resource_read` - Test resource reading
- `generate_test_cases` - Generate test cases from schemas

### Example Library
- `get_example_server` - Get example server code
- `get_pattern` - Get common patterns (auth, error-handling, etc.)

### Docs Generator
- `generate_api_docs` - Generate API documentation
- `generate_readme` - Generate README from config

### Deployment Helper
- `generate_dockerfile` - Generate Dockerfile
- `validate_deployment` - Validate deployment config

### Package Manager
- `check_dependencies` - Check dependency versions
- `suggest_dependencies` - Suggest dependencies based on features

## Examples

See the `examples/` directory for usage examples.

## Project Structure

```
dev-mcp-server/
├── README.md
├── requirements.txt
├── src/
│   ├── index.py                 # Main server entry point
│   ├── spec_reference/          # Spec reference tools
│   ├── scaffolder/              # Scaffolding tools
│   ├── code_generator/          # Code generation tools
│   ├── validator/               # Validation tools
│   ├── tester/                  # Testing tools
│   ├── example_library/         # Example library
│   ├── docs_generator/          # Documentation generation
│   ├── deployment_helper/        # Deployment tools
│   └── package_manager/         # Package management
└── examples/                    # Usage examples
```

## Documentation

For general MCP development documentation, see:
- [MCP Server Guide](../../docs/MCP_SERVER_GUIDE.md)
- [MCP Best Use Cases](../../docs/MCP_BEST_USE_CASES.md)

## Troubleshooting

See **[SETUP.md](../../SETUP.md)** for comprehensive troubleshooting guide.

**Common issues**:
- Import errors: Ensure venv is activated and dependencies are installed
- MCP client connection: Verify Python path in config and server starts correctly

## Contributing

Contributions welcome! Please ensure:
- Code follows Python best practices
- Tools are properly documented
- Examples are included for new features
