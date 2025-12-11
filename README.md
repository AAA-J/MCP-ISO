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
│   ├── discord-mcp-server/      # MCP server for Discord development
│   ├── app-docs/                # Internal documentation access
│   ├── app-db-readonly/         # Safe database read-only access
│   ├── app-api/                 # Backend API wrapper
│   ├── app-ops/                 # Observability and CI/CD integration
│   └── app-domain/              # Domain-specific business logic
└── examples/                    # General code examples and templates
```

## Available MCP Servers

Each MCP server has its own comprehensive README with installation and usage instructions.

### Development Tools

- **[Dev-MCP-Server](mcp-servers/dev-mcp-server/README.md)** - Tools for building MCP servers (scaffolding, code generation, validation, testing)
- **[Discord-MCP-Server](mcp-servers/discord-mcp-server/README.md)** - Tools for Discord development (apps, activities, social SDK)

### Custom SaaS App Servers

These servers are designed for greenfield SaaS applications and provide agents with controlled access to your application's internals:

- **[App-Docs Server](mcp-servers/app-docs/README.md)** - Internal documentation access. Exposes docs and specs as MCP resources with full-text search.
- **[App-DB-Readonly Server](mcp-servers/app-db-readonly/README.md)** - Safe database access. Provides read-only schema inspection and query execution with strict security.
- **[App-API Server](mcp-servers/app-api/README.md)** - Backend API wrapper. Wraps your REST/GraphQL API with typed tools for agents.
- **[App-Ops Server](mcp-servers/app-ops/README.md)** - Observability and CI/CD. Monitors pipelines, logs, and metrics with configurable adapters.
- **[App-Domain Server](mcp-servers/app-domain/README.md)** - Business logic shortcuts. Domain-specific tools configurable via YAML for your business operations.

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
