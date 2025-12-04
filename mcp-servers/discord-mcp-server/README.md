# Discord-MCP-Server

A Model Context Protocol (MCP) server that helps developers build Discord applications, Activities, and Social SDK integrations. This server provides tools for code generation, documentation access, and validation specific to Discord development.

## Features

- **Discord Apps** - Tools for building Discord bots and applications
- **Activities** - Tools for building Discord Activities
- **Social SDK** - Tools for integrating Discord Social SDK (C++, Unity, Unreal)

## Prerequisites

- Python 3.10+
- Discord Developer Account (for Discord API access)
- Basic understanding of Discord API

## Installation

See **[SETUP.md](../../SETUP.md)** for detailed setup instructions.

**Quick setup**:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Or use the automated setup script from repository root: `./setup.sh`

## Configuration

Create a `.env` file in this directory:

```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id
DISCORD_CLIENT_SECRET=your_client_secret
```

See [SETUP.md](../../SETUP.md) for instructions on getting Discord credentials.

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
    "discord-mcp-server": {
      "command": "python",
      "args": ["/path/to/mcp-servers/discord-mcp-server/src/index.py"],
      "env": {
        "DISCORD_TOKEN": "your_bot_token_here"
      }
    }
  }
}
```

If using venv, use the venv Python:

```json
{
  "mcpServers": {
    "discord-mcp-server": {
      "command": "/path/to/mcp-servers/discord-mcp-server/venv/bin/python",
      "args": ["src/index.py"],
      "env": {
        "DISCORD_TOKEN": "your_bot_token_here"
      }
    }
  }
}
```

## Available Tools

### Discord Apps

Tools for building Discord bots and applications:

- `discord_scaffold_app` - Generate Discord bot/application starter code
  - Supports TypeScript/JavaScript (discord.js) and Python (discord.py)
  - Generates project structure with common features
  
- `discord_generate_slash_command` - Generate slash command code
  - Creates command handler with proper schema
  - Supports options, choices, and validation
  
- `discord_generate_component` - Generate component code
  - Buttons, select menus, modals, text inputs
  - Proper event handling setup
  
- `discord_validate_interaction` - Validate interaction payloads
  - Checks against Discord API schema
  - Validates interaction types and data structures
  
- `discord_check_permissions` - Verify bot permissions
  - Checks if bot has required permissions
  - Suggests missing permissions

### Activities

Tools for building Discord Activities:

- `discord_generate_activity_starter` - Generate Activity starter code
  - React, vanilla JS, or Phaser frameworks
  - Embedded or iframe types
  - Multiplayer support
  
- `discord_generate_activity_layout` - Generate Activity layout code
  - Single-player, multiplayer, or spectator layouts
  - Responsive UI components
  
- `discord_generate_networking` - Generate multiplayer networking code
  - WebSocket, WebRTC, or Discord RPC transports
  - Real-time synchronization
  
- `discord_validate_activity_metadata` - Validate Activity metadata
  - Checks against Discord requirements
  - Validates assets and configuration

### Social SDK

Tools for Discord Social SDK integration:

- `discord_generate_sdk_init` - Generate SDK initialization code
  - C++, Unity, Unreal Engine, C#
  - Feature-specific initialization
  
- `discord_create_account_linking` - Generate account linking code
  - OAuth2 flow implementation
  - Provisional account support
  
- `discord_generate_rich_presence` - Generate rich presence code
  - Game, streaming, listening, watching presences
  - Custom assets and timestamps
  
- `discord_validate_oauth_scopes` - Validate OAuth2 scopes
  - Checks required scopes for use cases
  - Validates scope combinations

## Project Structure

```
discord-mcp-server/
├── README.md
├── requirements.txt
├── src/
│   ├── index.py                 # Main server entry point
│   ├── apps/                    # Discord apps tools
│   ├── activities/              # Activities tools
│   └── social_sdk/             # Social SDK tools
├── docs/
│   └── DISCORD_DEV_DOCS.md     # Discord API documentation reference
└── examples/                    # Usage examples
```

## Documentation

- [Discord Developer Documentation](docs/DISCORD_DEV_DOCS.md) - Comprehensive Discord API reference
- [Discord Developer Portal](https://discord.com/developers) - Official Discord developer resources

## Examples

See the `examples/` directory for usage examples:
- Scaffolding a Discord bot
- Creating slash commands
- Building Activities
- Integrating Social SDK

## Troubleshooting

See **[SETUP.md](../../SETUP.md)** for comprehensive troubleshooting guide.

**Common issues**:
- Import errors: Ensure venv is activated and dependencies are installed
- Discord API errors: Verify `.env` file exists and tokens are correct
- MCP client connection: Verify Python path in config and server starts correctly

## Contributing

Contributions welcome! Please ensure:
- Code follows Python best practices
- Tools are properly documented
- Examples are included for new features
- Discord API best practices are followed
