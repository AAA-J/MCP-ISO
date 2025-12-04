# How to Create a Discord MCP Server

This guide walks you through creating a Model Context Protocol (MCP) server that integrates with Discord's API.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Understanding MCP Servers](#understanding-mcp-servers)
3. [Setting Up Discord Application](#setting-up-discord-application)
4. [Project Structure](#project-structure)
5. [Implementation Guide](#implementation-guide)
6. [Authentication](#authentication)
7. [Implementing Tools](#implementing-tools)
8. [Implementing Resources](#implementing-resources)
9. [Testing Your Server](#testing-your-server)
10. [Deployment](#deployment)

---

## Prerequisites

- Node.js 18+ or Python 3.10+
- Discord Developer Account
- Basic understanding of REST APIs and JSON-RPC
- Familiarity with Discord API (see [DISCORD_DEV_DOCS.md](./DISCORD_DEV_DOCS.md))

---

## Understanding MCP Servers

An MCP server exposes three main capabilities:

1. **Tools** - Functions the AI can call to perform actions
2. **Resources** - Data sources the AI can read
3. **Prompts** - Reusable prompt templates

MCP servers communicate using JSON-RPC 2.0 over stdio (standard input/output) or HTTP/SSE.

### Key Concepts

- **JSON-RPC 2.0**: The communication protocol
- **Transport**: How messages are sent (stdio, HTTP, SSE)
- **Capabilities**: What your server can do (tools, resources, prompts)
- **Authentication**: How to securely access Discord's API

---

## Setting Up Discord Application

### Step 1: Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name your application (e.g., "My MCP Server")
4. Note your **Application ID**

### Step 2: Create a Bot

1. Navigate to the "Bot" section
2. Click "Add Bot"
3. Copy the **Bot Token** (keep this secret!)
4. Enable these Privileged Gateway Intents if needed:
   - MESSAGE CONTENT INTENT
   - PRESENCE INTENT
   - SERVER MEMBERS INTENT

### Step 3: Set Up OAuth2 (for user authentication)

1. Go to "OAuth2" section
2. Add redirect URI: `http://localhost:3000/callback` (or your server URL)
3. Note your **Client ID** and **Client Secret**
4. Select required scopes:
   - `bot` - For bot commands
   - `guilds` - Read guild information
   - `messages.read` - Read messages
   - `messages.write` - Send messages
   - `channels.read` - Read channel information
   - `guilds.members.read` - Read member information

### Step 4: Invite Bot to Server

1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`
3. Select permissions:
   - Send Messages
   - Read Message History
   - Manage Messages
   - Read Messages/View Channels
4. Copy the generated URL and open it to invite the bot

---

## Project Structure

### TypeScript/Node.js Structure

```
discord-mcp-server/
├── src/
│   ├── index.ts              # Main server entry point
│   ├── discord/
│   │   ├── client.ts         # Discord API client
│   │   ├── auth.ts           # Authentication handling
│   │   └── types.ts          # TypeScript types
│   ├── tools/
│   │   ├── messages.ts       # Message-related tools
│   │   ├── channels.ts       # Channel-related tools
│   │   └── guilds.ts         # Guild-related tools
│   ├── resources/
│   │   ├── channels.ts       # Channel resources
│   │   └── messages.ts       # Message resources
│   └── prompts/
│       └── discord.ts         # Prompt templates
├── package.json
├── tsconfig.json
└── .env.example
```

### Python Structure

```
discord-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py             # Main server entry point
│   ├── discord/
│   │   ├── client.py         # Discord API client
│   │   ├── auth.py           # Authentication handling
│   │   └── types.py          # Type definitions
│   ├── tools/
│   │   ├── messages.py       # Message-related tools
│   │   ├── channels.py       # Channel-related tools
│   │   └── guilds.py         # Guild-related tools
│   ├── resources/
│   │   ├── channels.py       # Channel resources
│   │   └── messages.py       # Message resources
│   └── prompts/
│       └── discord.py         # Prompt templates
├── requirements.txt
├── pyproject.toml
└── .env.example
```

---

## Implementation Guide

### TypeScript Implementation

#### 1. Install Dependencies

```bash
npm init -y
npm install @modelcontextprotocol/sdk discord.js dotenv
npm install -D typescript @types/node ts-node
```

#### 2. Create package.json Scripts

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts"
  }
}
```

#### 3. Basic Server Structure (src/index.ts)

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { 
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// Initialize server
const server = new Server(
  {
    name: 'discord-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'send_message',
        description: 'Send a message to a Discord channel',
        inputSchema: {
          type: 'object',
          properties: {
            channelId: {
              type: 'string',
              description: 'The Discord channel ID',
            },
            content: {
              type: 'string',
              description: 'The message content',
            },
          },
          required: ['channelId', 'content'],
        },
      },
      // Add more tools...
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'send_message':
      // Implement Discord API call
      return {
        content: [
          {
            type: 'text',
            text: `Message sent to channel ${args.channelId}`,
          },
        ],
      };
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// List resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: 'discord://channels',
        name: 'Discord Channels',
        description: 'List of Discord channels',
        mimeType: 'application/json',
      },
      // Add more resources...
    ],
  };
});

// Read resources
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri.startsWith('discord://channels')) {
    // Fetch channels from Discord API
    return {
      contents: [
        {
          uri,
          mimeType: 'application/json',
          text: JSON.stringify({ channels: [] }, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Discord MCP server running on stdio');
}

main().catch(console.error);
```

### Python Implementation

#### 1. Install Dependencies

```bash
pip install mcp discord.py python-dotenv aiohttp
```

#### 2. Basic Server Structure (src/server.py)

```python
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, Resource, TextContent
from discord import Client, Intents

# Initialize Discord client
intents = Intents.default()
intents.message_content = True
discord_client = Client(intents=intents)

# Initialize MCP server
server = Server("discord-mcp-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="send_message",
            description="Send a message to a Discord channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channelId": {
                        "type": "string",
                        "description": "The Discord channel ID"
                    },
                    "content": {
                        "type": "string",
                        "description": "The message content"
                    }
                },
                "required": ["channelId", "content"]
            }
        ),
        # Add more tools...
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "send_message":
        channel_id = arguments.get("channelId")
        content = arguments.get("content")
        
        # Implement Discord API call
        channel = discord_client.get_channel(int(channel_id))
        if channel:
            await channel.send(content)
            return [TextContent(
                type="text",
                text=f"Message sent to channel {channel_id}"
            )]
        else:
            raise ValueError(f"Channel {channel_id} not found")
    
    raise ValueError(f"Unknown tool: {name}")

@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="discord://channels",
            name="Discord Channels",
            description="List of Discord channels",
            mimeType="application/json"
        ),
        # Add more resources...
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri.startswith("discord://channels"):
        # Fetch channels from Discord API
        channels = [{"id": str(ch.id), "name": ch.name} 
                   for ch in discord_client.get_all_channels()]
        return json.dumps({"channels": channels}, indent=2)
    
    raise ValueError(f"Unknown resource: {uri}")

async def main():
    # Start Discord client
    await discord_client.start(os.getenv("DISCORD_TOKEN"))
    
    # Start MCP server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Authentication

### Bot Token Authentication

For bot operations, use the bot token:

```typescript
// TypeScript
import { REST } from '@discordjs/rest';
import { Routes } from 'discord-api-types/v10';

const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN!);
```

```python
# Python
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.run(os.getenv('DISCORD_TOKEN'))
```

### OAuth2 User Authentication

For user-scoped operations, implement OAuth2 flow:

1. Generate authorization URL
2. Redirect user to Discord
3. Handle callback with authorization code
4. Exchange code for access token
5. Store token securely

See [Discord OAuth2 Documentation](https://discord.com/developers/docs/topics/oauth2)

---

## Implementing Tools

Tools are functions the AI can call. Here are examples:

### Message Tools

```typescript
// Send message
{
  name: 'send_message',
  description: 'Send a message to a Discord channel',
  inputSchema: {
    type: 'object',
    properties: {
      channelId: { type: 'string' },
      content: { type: 'string' },
      embed: { type: 'object' }, // Optional
    },
    required: ['channelId', 'content'],
  },
}

// Edit message
{
  name: 'edit_message',
  description: 'Edit an existing Discord message',
  inputSchema: {
    type: 'object',
    properties: {
      channelId: { type: 'string' },
      messageId: { type: 'string' },
      content: { type: 'string' },
    },
    required: ['channelId', 'messageId', 'content'],
  },
}

// Delete message
{
  name: 'delete_message',
  description: 'Delete a Discord message',
  inputSchema: {
    type: 'object',
    properties: {
      channelId: { type: 'string' },
      messageId: { type: 'string' },
    },
    required: ['channelId', 'messageId'],
  },
}
```

### Channel Tools

```typescript
// Create channel
{
  name: 'create_channel',
  description: 'Create a new Discord channel',
  inputSchema: {
    type: 'object',
    properties: {
      guildId: { type: 'string' },
      name: { type: 'string' },
      type: { type: 'number', enum: [0, 2, 4, 5] }, // TEXT, VOICE, CATEGORY, NEWS
    },
    required: ['guildId', 'name'],
  },
}

// List channels
{
  name: 'list_channels',
  description: 'List all channels in a guild',
  inputSchema: {
    type: 'object',
    properties: {
      guildId: { type: 'string' },
    },
    required: ['guildId'],
  },
}
```

### Guild Tools

```typescript
// Get guild info
{
  name: 'get_guild',
  description: 'Get information about a Discord guild',
  inputSchema: {
    type: 'object',
    properties: {
      guildId: { type: 'string' },
    },
    required: ['guildId'],
  },
}

// List guild members
{
  name: 'list_members',
  description: 'List members in a Discord guild',
  inputSchema: {
    type: 'object',
    properties: {
      guildId: { type: 'string' },
      limit: { type: 'number', default: 100 },
    },
    required: ['guildId'],
  },
}
```

---

## Implementing Resources

Resources provide read-only data access:

```typescript
// Channel resource
{
  uri: 'discord://channel/{channelId}',
  name: 'Discord Channel',
  description: 'Information about a specific Discord channel',
  mimeType: 'application/json',
}

// Message resource
{
  uri: 'discord://channel/{channelId}/messages',
  name: 'Channel Messages',
  description: 'Messages in a Discord channel',
  mimeType: 'application/json',
}

// Guild resource
{
  uri: 'discord://guild/{guildId}',
  name: 'Discord Guild',
  description: 'Information about a Discord guild',
  mimeType: 'application/json',
}
```

---

## Testing Your Server

### 1. Environment Setup

Create `.env` file:

```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id
DISCORD_CLIENT_SECRET=your_client_secret
```

### 2. Run the Server

```bash
# TypeScript
npm run dev

# Python
python src/server.py
```

### 3. Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

### 4. Test Tool Calls

Use the MCP Inspector to:
- List available tools
- Call tools with test parameters
- Verify responses
- Check error handling

---

## Deployment

### Local Development (stdio)

MCP servers typically run via stdio for local development. Configure your MCP client:

```json
{
  "mcpServers": {
    "discord": {
      "command": "node",
      "args": ["/path/to/dist/index.js"],
      "env": {
        "DISCORD_TOKEN": "your_token"
      }
    }
  }
}
```

### HTTP Server (for remote access)

For production, you can expose your MCP server over HTTP:

```typescript
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import express from 'express';

const app = express();
const transport = new SSEServerTransport('/mcp', app);

await server.connect(transport);
app.listen(3000);
```

---

## Best Practices

1. **Error Handling**: Always handle Discord API errors gracefully
2. **Rate Limiting**: Respect Discord's rate limits (see [Rate Limits](https://discord.com/developers/docs/topics/rate-limits))
3. **Security**: Never expose tokens or secrets
4. **Validation**: Validate all inputs before making API calls
5. **Logging**: Log important operations for debugging
6. **Documentation**: Document all tools and resources clearly

---

## Next Steps

1. Review [DISCORD_DEV_DOCS.md](./DISCORD_DEV_DOCS.md) for API details
2. Implement additional tools based on your needs
3. Add error handling and validation
4. Set up proper authentication flow
5. Test thoroughly before deployment
6. Consider adding prompts for common Discord operations

---

## Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [Discord API Documentation](https://discord.com/developers/docs)
- [Discord.js Documentation](https://discord.js.org) (TypeScript)
- [discord.py Documentation](https://discordpy.readthedocs.io) (Python)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

## Example: Complete Tool Implementation

Here's a complete example of implementing a `send_message` tool:

```typescript
import { REST } from '@discordjs/rest';
import { Routes } from 'discord-api-types/v10';

const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN!);

async function sendMessage(channelId: string, content: string) {
  try {
    const message = await rest.post(Routes.channelMessages(channelId), {
      body: { content },
    });
    
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            messageId: message.id,
            channelId: message.channel_id,
            content: message.content,
          }, null, 2),
        },
      ],
    };
  } catch (error: any) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: false,
            error: error.message,
            code: error.code,
          }, null, 2),
        },
      ],
      isError: true,
    };
  }
}
```

This guide provides a foundation for building your Discord MCP server. Refer to the Discord API documentation for specific endpoint details and requirements.

