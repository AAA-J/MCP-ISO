# Application Integration Servers

This directory contains MCP servers designed for integrating AI agents with your SaaS application's internals. These servers provide controlled, secure access to your application's documentation, database, APIs, operations, and domain logic.

## Available Servers

### [app-docs](./app-docs/README.md)
Internal documentation access. Exposes your documentation and specifications as MCP resources with full-text search capabilities.

**Use when**: You want AI agents to access your internal documentation, specs, and diagrams.

### [app-db-readonly](./app-db-readonly/README.md)
Safe database access. Provides read-only schema inspection and query execution with strict security controls.

**Use when**: You need AI agents to query your database safely without write access.

### [app-api](./app-api/README.md)
Backend API wrapper. Wraps your REST/GraphQL API with typed tools for agents to interact with your backend.

**Use when**: You want AI agents to call your backend APIs in a controlled, typed manner.

### [app-ops](./app-ops/README.md)
Observability and CI/CD integration. Monitors pipelines, logs, and metrics with configurable adapters for different platforms.

**Use when**: You need AI agents to monitor your application's health, CI/CD pipelines, and observability data.

### [app-domain](./app-domain/README.md)
Business logic shortcuts. Provides domain-specific tools configurable via YAML for your business operations.

**Use when**: You want to expose custom business logic and domain-specific operations to AI agents.

## Setup

Each server is self-contained. Navigate to the server directory and follow its README for setup instructions.

```bash
cd application/[server-name]
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Setup

Use the setup script for application servers:

```bash
./scripts/setup_custom_servers.sh
```

Or use the main setup script from the repository root:

```bash
./setup.sh
```

## Configuration

Each application server requires specific environment variables. See each server's README for configuration details. You'll typically configure these in your IDE's MCP configuration file (`~/.cursor/mcp.json`).

## Architecture

These servers are designed to work together as a complete integration layer:

- **app-docs**: Provides context about your application
- **app-db-readonly**: Provides data access
- **app-api**: Provides API interaction
- **app-ops**: Provides operational visibility
- **app-domain**: Provides business logic shortcuts

You can use one or all of them depending on your needs.

