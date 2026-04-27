# MCP-ISO

**MCP-ISO** helps developers create MCP (Model Context Protocol) servers while serving as an organized archive of MCP server implementations.

## Purpose

1. **Help developers build MCP servers** - Tools, documentation, and examples
2. **Archive of MCP servers** - Collection of MCP server implementations

## Start in 5 Minutes

**Happy path — single command, then verify:**

```bash
# 1. Clone and enter the repo
git clone https://github.com/your-username/MCP-ISO.git && cd MCP-ISO

# 2. Run the automated setup (Python 3.10+ required)
./setup.sh

# 3. Verify everything is wired correctly
./scripts/check_mcp_servers.sh
```

That's it. When `check_mcp_servers.sh` shows all green, copy `mcp.example.json` into your `~/.cursor/mcp.json`, update the `/path/to/` placeholders, and restart your IDE.

> Need the full walkthrough or troubleshooting help? See **[SETUP.md](SETUP.md)** and **[VERIFY_MCP_SERVERS.md](VERIFY_MCP_SERVERS.md)**.
>
> Not sure which servers to enable? See the [stack profiles](docs/stack-profiles/README.md) — pick Solo, Startup, or Enterprise and use the matching `mcp.json` snippet.

---

## Quick Start

See **[SETUP.md](SETUP.md)** for complete setup instructions.

```bash
# Quick setup (automated)
./setup.sh

# Or manual setup
cd mcp-servers/development/[server-name]  # or application/[server-name]
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
├── VERIFY_MCP_SERVERS.md        # Guide to verify MCP servers are running
├── setup.sh                     # Automated setup script
├── requirements.txt             # Root Python dependencies
├── docs/                        # General MCP development documentation
│   ├── MCP_SERVER_GUIDE.md     # Guide for creating MCP servers
│   ├── MCP_BEST_USE_CASES.md   # Best practices and patterns
│   └── IDE_AI_AGENT_COMPONENTS_STANDARD.md # Standard component model and MCP minimum sets
├── scripts/                     # Utility scripts
│   ├── check_mcp_servers.sh    # Verify MCP server configuration
│   ├── fix_mcp_servers.sh      # Fix common setup issues
│   └── setup_custom_servers.sh # Setup custom app servers
├── mcp-servers/                 # Archive of MCP server implementations
│   ├── development/             # Development tools and utilities
│   │   ├── dev-mcp-server/     # MCP server for building MCP servers
│   │   └── discord-mcp-server/  # MCP server for Discord development
│   └── application/             # Application integration servers
│       ├── app-docs/            # Internal documentation access
│       ├── app-db-readonly/     # Safe database read-only access
│       ├── app-api/             # Backend API wrapper
│       ├── app-ops/             # Observability and CI/CD integration
│       └── app-domain/          # Domain-specific business logic
└── examples/                    # General code examples and templates
```

## Available MCP Servers

Each MCP server has its own comprehensive README with installation and usage instructions.

### Development Tools

Located in `mcp-servers/development/`:

- **[Dev-MCP-Server](mcp-servers/development/dev-mcp-server/README.md)** - Tools for building MCP servers (scaffolding, code generation, validation, testing)
- **[Discord-MCP-Server](mcp-servers/development/discord-mcp-server/README.md)** - Tools for Discord development (apps, activities, social SDK)

### Application Integration Servers

Located in `mcp-servers/application/`. These servers are designed for greenfield SaaS applications and provide agents with controlled access to your application's internals:

- **[App-Docs Server](mcp-servers/application/app-docs/README.md)** - Internal documentation access. Exposes docs and specs as MCP resources with full-text search.
- **[App-DB-Readonly Server](mcp-servers/application/app-db-readonly/README.md)** - Safe database access. Provides read-only schema inspection and query execution with strict security.
- **[App-API Server](mcp-servers/application/app-api/README.md)** - Backend API wrapper. Wraps your REST/GraphQL API with typed tools for agents.
- **[App-Ops Server](mcp-servers/application/app-ops/README.md)** - Observability and CI/CD. Monitors pipelines, logs, and metrics with configurable adapters.
- **[App-Domain Server](mcp-servers/application/app-domain/README.md)** - Business logic shortcuts. Domain-specific tools configurable via YAML for your business operations.

## Documentation

- **[AI CI/CD Guidelines](AI_CI_CD_GUIDELINES.md)** - CI/CD checklist for AI assistants (read this first!)
- **[Setup Guide](SETUP.md)** - Complete setup instructions
- **[Migration Guide](MIGRATION.md)** - Guide for updating after repository reorganization
- **[Verify MCP Servers](VERIFY_MCP_SERVERS.md)** - Guide to verify MCP servers are running correctly
- [MCP Server Guide](docs/MCP_SERVER_GUIDE.md) - Guide to creating MCP servers
- [MCP Best Use Cases](docs/MCP_BEST_USE_CASES.md) - Best practices and patterns
- [IDE AI Agent Components Standard](docs/IDE_AI_AGENT_COMPONENTS_STANDARD.md) - 6 standard + 4 emerging components, minimum MCP sets, and stack decision tree
- [Server Quality Bar](docs/SERVER_QUALITY_BAR.md) - Health check, test, auth, and ownership standards per server
- [Stack Profiles](docs/stack-profiles/README.md) - Concrete `mcp.json` examples for Solo, Startup, and Enterprise
- [Discord Upstream Update Plan](docs/DISCORD_UPSTREAM_UPDATE_PLAN.md) - Process for tracking Discord docs/API changes and safely updating `discord-mcp-server`

## Utility Scripts

The `scripts/` directory contains helpful utilities:

- **`scripts/check_mcp_servers.sh`** - Verify MCP server configuration and setup
- **`scripts/fix_mcp_servers.sh`** - Fix common setup issues (Python version, dependencies)
- **`scripts/setup_custom_servers.sh`** - Setup all custom app servers (app-docs, app-db-readonly, etc.)

Usage:
```bash
# Check server configuration
./scripts/check_mcp_servers.sh

# Fix setup issues
./scripts/fix_mcp_servers.sh

# Setup custom servers
./scripts/setup_custom_servers.sh
```

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Discord Developer Portal](https://discord.com/developers)

---

**Note**: Each MCP server is self-contained with its own README, requirements, and documentation. See [SETUP.md](SETUP.md) for detailed setup instructions.
