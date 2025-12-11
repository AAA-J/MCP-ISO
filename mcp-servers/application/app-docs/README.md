# App-Docs MCP Server

MCP server for accessing internal documentation and specifications. Makes all your internal docs easily accessible to AI agents.

## Features

- **Documentation Resources**: Expose markdown files as MCP resources
- **Full-Text Search**: Search across all documentation files
- **Diagram Support**: Retrieve diagram files (SVG, PNG, PDF, etc.)
- **Auto-Discovery**: Automatically discovers all `.md` files in your docs directory

## Installation

```bash
cd mcp-servers/application/app-docs
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `application/app-docs` directory:

```env
# Base directory where documentation is located (default: current working directory)
BASE_DIR=.

# Documentation directory relative to BASE_DIR (default: docs)
DOCS_DIR=docs
```

## Usage

### Running the Server

```bash
python src/index.py
```

### Configuring in MCP Client

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "app-docs": {
      "command": "python",
      "args": ["/path/to/mcp-servers/application/app-docs/src/index.py"],
      "env": {
        "BASE_DIR": "/path/to/your/project",
        "DOCS_DIR": "docs"
      }
    }
  }
}
```

## Available Tools

### `search_docs`

Search across all documentation files for a query string.

**Parameters:**
- `query` (required): Search query string
- `limit` (optional): Maximum number of results to return (default: 10)

**Example:**
```json
{
  "query": "authentication",
  "limit": 5
}
```

### `get_diagram`

Retrieve a diagram file by name.

**Parameters:**
- `name` (required): Name or path of the diagram file

**Example:**
```json
{
  "name": "architecture-diagram"
}
```

## Available Resources

Resources are automatically discovered from your documentation directory:

- `app-docs://docs/{filename}` - Markdown documentation files
- `app-docs://diagrams/{filename}` - Diagram files (SVG, PNG, PDF, etc.)

The server automatically discovers:
- Root-level files: `AGENTS.md`, `AI.md`, `README.md`
- All `.md` files in the `docs/` directory
- Diagram files (SVG, PNG, JPG, GIF, PDF) in the `docs/` directory

## Security

- **Read-Only Access**: The server only reads files, never modifies them
- **Path Validation**: All file paths are validated to prevent directory traversal
- **No Sensitive Data**: Ensure your documentation doesn't contain sensitive information

## Examples

See the `examples/` directory for usage examples.

## Troubleshooting

**No documentation found:**
- Check that `BASE_DIR` and `DOCS_DIR` are set correctly
- Verify the documentation directory exists and contains `.md` files

**Search returns no results:**
- Ensure your documentation files are readable
- Try a simpler search query

