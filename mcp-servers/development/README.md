# Development Tools

This directory contains MCP servers designed for development and tooling purposes.

## Available Servers

### [dev-mcp-server](./dev-mcp-server/README.md)
Tools for building MCP servers. Provides scaffolding, code generation, validation, testing, and deployment helpers.

**Use when**: You want to create, test, or maintain MCP servers.

### [discord-mcp-server](./discord-mcp-server/README.md)
Tools for Discord development. Provides tools for creating Discord apps, activities, and working with the Discord Social SDK.

**Use when**: You're building Discord bots, apps, or integrations.

## Setup

Each server is self-contained. Navigate to the server directory and follow its README for setup instructions.

```bash
cd development/[server-name]
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Setup

Use the main setup script from the repository root:

```bash
./setup.sh
```

This will set up all development tools automatically.

