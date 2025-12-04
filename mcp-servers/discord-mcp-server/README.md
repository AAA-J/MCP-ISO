# Discord-MCP-Server

A Model Context Protocol (MCP) server that helps developers build Discord applications, Activities, and Social SDK integrations. This server provides tools for code generation, documentation access, and validation specific to Discord development.

## Features

- **Discord Apps** - Tools for building Discord bots and applications
- **Activities** - Tools for building Discord Activities
- **Social SDK** - Tools for integrating Discord Social SDK (C++, Unity, Unreal)

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

## Available Tools

### Discord Apps
- `discord_scaffold_app` - Generate Discord bot/application starter code
- `discord_generate_slash_command` - Generate slash command code
- `discord_generate_component` - Generate component code (buttons, modals, etc.)
- `discord_validate_interaction` - Validate interaction payloads
- `discord_check_permissions` - Verify bot permissions

### Activities
- `discord_generate_activity_starter` - Generate Activity starter code
- `discord_generate_activity_layout` - Generate Activity layout code
- `discord_generate_networking` - Generate multiplayer networking code
- `discord_validate_activity_metadata` - Validate Activity metadata

### Social SDK
- `discord_generate_sdk_init` - Generate SDK initialization code
- `discord_create_account_linking` - Generate account linking code
- `discord_generate_rich_presence` - Generate rich presence code
- `discord_validate_oauth_scopes` - Validate OAuth2 scopes

## Documentation

See `docs/DISCORD_DEV_DOCS.md` for comprehensive Discord API documentation references.

## Examples

See the `examples/` directory for usage examples.

