# MCP-ISO

**MCP-ISO** helps developers create MCP (Model Context Protocol) servers while serving as an organized archive of MCP server implementations. The repository provides both documentation and code examples, structured for easy use by both AI assistants and human developers.

## Purpose

This repository serves two main purposes:

1. **Help developers build MCP servers** - Provides tools, documentation, and examples for creating MCP servers
2. **Archive of MCP servers** - Maintains a collection of MCP server implementations for reference and reuse

## Repository Structure

```
MCP-ISO/
├── README.md                    # This file
├── requirements.txt             # Root Python dependencies
├── docs/                        # General MCP development documentation
│   ├── MCP_SERVER_GUIDE.md     # Guide for creating MCP servers
│   └── MCP_BEST_USE_CASES.md   # Best practices and patterns
├── mcp-servers/                 # Archive of MCP server implementations
│   ├── dev-mcp-server/         # MCP server for building MCP servers
│   └── discord-mcp-server/      # MCP server for Discord development
└── examples/                    # General code examples and templates
```

## Quick Start

### Prerequisites

- Python 3.10+ or Node.js 18+
- Basic understanding of JSON-RPC 2.0
- Familiarity with REST APIs

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/MCP-ISO.git
cd MCP-ISO
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Available MCP Servers

### 1. Dev-MCP-Server

**Purpose**: Helps developers build MCP servers

**Location**: `mcp-servers/dev-mcp-server/`

**Features**:
- **Spec Reference** - Access MCP specification and best practices
- **Scaffolder** - Generate starter project structures
- **Code Generator** - Generate tool handlers, resources, and prompts
- **Tester** - Test MCP servers without manual setup
- **Example Library** - Reference implementations and patterns
- **Validator** - Validate MCP server compliance
- **Docs Generator** - Generate documentation from code
- **Deployment Helper** - Prepare MCP servers for deployment
- **Package Manager** - Manage dependencies and versions

**Usage**:
```bash
cd mcp-servers/dev-mcp-server
pip install -r requirements.txt
python src/index.py
```

**Documentation**: See [dev-mcp-server/README.md](mcp-servers/dev-mcp-server/README.md)

### 2. Discord-MCP-Server

**Purpose**: Helps developers build Discord applications, Activities, and Social SDK integrations

**Location**: `mcp-servers/discord-mcp-server/`

**Features**:
- **Discord Apps** - Tools for building Discord bots and applications
- **Activities** - Tools for building Discord Activities
- **Social SDK** - Tools for integrating Discord Social SDK (C++, Unity, Unreal)

**Usage**:
```bash
cd mcp-servers/discord-mcp-server
pip install -r requirements.txt
python src/index.py
```

**Documentation**: See [discord-mcp-server/README.md](mcp-servers/discord-mcp-server/README.md)

## How to Use This Repository

### For Developers Building MCP Servers

1. **Read the Documentation**:
   - Start with [MCP Server Guide](docs/MCP_SERVER_GUIDE.md)
   - Review [Best Use Cases](docs/MCP_BEST_USE_CASES.md)

2. **Use Dev-MCP-Server**:
   - Scaffold a new MCP server project
   - Generate code templates
   - Validate your implementation
   - Test your server

3. **Reference Examples**:
   - Check `examples/` directory
   - Review existing MCP servers in `mcp-servers/`

### For Developers Building Discord Applications

1. **Use Discord-MCP-Server**:
   - Generate Discord bot code
   - Create Activity starters
   - Build Social SDK integrations

2. **Reference Documentation**:
   - See [Discord Developer Docs](mcp-servers/discord-mcp-server/docs/DISCORD_DEV_DOCS.md)
   - Review code examples in `mcp-servers/discord-mcp-server/examples/`

### For AI Assistants

The repository structure is designed for easy navigation:

- **Clear directory structure** - Each MCP server is self-contained
- **Comprehensive READMEs** - Each server has its own README
- **Structured documentation** - Markdown files with clear headings
- **Code examples** - Examples directory in each server

## Adding New MCP Servers to Archive

To add a new MCP server to the archive:

1. Create a new directory in `mcp-servers/`:
```bash
mkdir -p mcp-servers/your-mcp-server/{src,docs,examples}
```

2. Follow the structure:
   - `README.md` - Server documentation
   - `requirements.txt` - Python dependencies (if applicable)
   - `src/` - Source code
   - `docs/` - Documentation
   - `examples/` - Code examples

3. Update this README to include your new server

## Documentation

- [MCP Server Guide](docs/MCP_SERVER_GUIDE.md) - Complete guide to creating MCP servers
- [MCP Best Use Cases](docs/MCP_BEST_USE_CASES.md) - Best practices and patterns
- [Discord Developer Docs](mcp-servers/discord-mcp-server/docs/DISCORD_DEV_DOCS.md) - Discord API reference

## Requirements

See [requirements.txt](requirements.txt) for root-level dependencies.

Each MCP server has its own `requirements.txt` with specific dependencies.

## Contributing

Contributions are welcome! Please:

1. Follow the existing repository structure
2. Include comprehensive documentation
3. Add examples for new features
4. Update this README when adding new servers

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Discord Developer Portal](https://discord.com/developers)

## License

[Add your license here]

---

**Note**: This repository is designed to be both AI and human-friendly. Clear structure, comprehensive documentation, and organized code examples make it easy to navigate and use.
