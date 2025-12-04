# MCP-ISO

**MCP-ISO** helps developers create MCP (Model Context Protocol) servers while serving as an organized archive of MCP server implementations.

## Purpose

1. **Help developers build MCP servers** - Tools, documentation, and examples
2. **Archive of MCP servers** - Collection of MCP server implementations

## Quick Start

See **[SETUP.md](SETUP.md)** for complete setup instructions.

```bash
# Quick setup (automated)
./setup.sh

# Or manual setup
cd mcp-servers/[server-name]
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Repository Structure

```
MCP-ISO/
├── README.md                    # This file
├── AI_CI_CD_GUIDELINES.md      # CI/CD guidelines for AI assistants
├── SETUP.md                     # Setup guide
├── setup.sh                     # Automated setup script
├── requirements.txt             # Root Python dependencies
├── docs/                        # General MCP development documentation
│   ├── MCP_SERVER_GUIDE.md     # Guide for creating MCP servers
│   └── MCP_BEST_USE_CASES.md   # Best practices and patterns
├── mcp-servers/                 # Archive of MCP server implementations
│   ├── dev-mcp-server/         # MCP server for building MCP servers
│   └── discord-mcp-server/      # MCP server for Discord development
└── examples/                    # General code examples and templates
```

## Available MCP Servers

Each MCP server has its own comprehensive README with installation and usage instructions.

- **[Dev-MCP-Server](mcp-servers/dev-mcp-server/README.md)** - Tools for building MCP servers (scaffolding, code generation, validation, testing)
- **[Discord-MCP-Server](mcp-servers/discord-mcp-server/README.md)** - Tools for Discord development (apps, activities, social SDK)

## Documentation

- **[AI CI/CD Guidelines](AI_CI_CD_GUIDELINES.md)** - CI/CD checklist for AI assistants (read this first!)
- **[Setup Guide](SETUP.md)** - Complete setup instructions
- [MCP Server Guide](docs/MCP_SERVER_GUIDE.md) - Guide to creating MCP servers
- [MCP Best Use Cases](docs/MCP_BEST_USE_CASES.md) - Best practices and patterns

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Discord Developer Portal](https://discord.com/developers)

---

**Note**: Each MCP server is self-contained with its own README, requirements, and documentation. See [SETUP.md](SETUP.md) for detailed setup instructions.
