# MCP-ISO Setup Guide

This guide walks you through setting up the MCP-ISO repository and its MCP servers.

## Prerequisites

- Python 3.10+ or Node.js 18+
- Git
- Basic understanding of MCP (Model Context Protocol)

## Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/MCP-ISO.git
cd MCP-ISO
```

### 2. Choose Your MCP Server

Each MCP server is self-contained. Navigate to the server directory:

- **Dev-MCP-Server**: `cd mcp-servers/dev-mcp-server`
- **Discord-MCP-Server**: `cd mcp-servers/discord-mcp-server`

### 3. Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Setting Up Individual MCP Servers

### Dev-MCP-Server

**Purpose**: Tools for building MCP servers

**Setup**:
```bash
cd mcp-servers/dev-mcp-server
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**No environment variables needed** - This server doesn't require external API keys.

**Test**:
```bash
python src/index.py
```

**MCP Client Configuration**:
```json
{
  "mcpServers": {
    "dev-mcp-server": {
      "command": "/path/to/mcp-servers/dev-mcp-server/venv/bin/python",
      "args": ["src/index.py"]
    }
  }
}
```

### Discord-MCP-Server

**Purpose**: Tools for Discord development (apps, activities, social SDK)

**Setup**:
```bash
cd mcp-servers/discord-mcp-server
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Environment Variables**:

Create a `.env` file in `mcp-servers/discord-mcp-server/`:

```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_CLIENT_ID=your_client_id
DISCORD_CLIENT_SECRET=your_client_secret
```

**Getting Discord Credentials**:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select existing one
3. Go to "Bot" section → Copy bot token
4. Go to "OAuth2" section → Copy Client ID and Client Secret

**Test**:
```bash
python src/index.py
```

**MCP Client Configuration**:
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

## Installing MCP Servers into Your IDE

After setting up your MCP server locally, you need to configure your IDE to use it. The process varies by IDE, but follows these general steps:

### Prerequisites

Before configuring your IDE, ensure you have:

1. ✅ Completed the server setup (virtual environment created, dependencies installed)
2. ✅ Tested the server manually (it should start without errors)
3. ✅ Located the absolute path to your server's Python executable and script

### Finding Required Paths

You'll need these paths for IDE configuration:

**Python Executable Path:**
- **macOS/Linux**: `/full/path/to/mcp-servers/[server-name]/venv/bin/python`
- **Windows**: `C:\full\path\to\mcp-servers\[server-name]\venv\Scripts\python.exe`

**Server Script Path:**
- **macOS/Linux**: `/full/path/to/mcp-servers/[server-name]/src/index.py`
- **Windows**: `C:\full\path\to\mcp-servers\[server-name]\src\index.py`

**To find your paths:**

```bash
# Get absolute path to Python executable (run from server directory)
cd mcp-servers/dev-mcp-server  # or discord-mcp-server
source venv/bin/activate  # or venv\Scripts\activate on Windows
which python  # macOS/Linux
# or
where python  # Windows

# Get absolute path to server script
pwd  # Shows current directory
# Then append: /src/index.py
```

### Configuration Format

Your IDE will need a configuration file (usually JSON) with this structure:

**For Dev-MCP-Server:**
```json
{
  "mcpServers": {
    "dev-mcp-server": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/mcp-servers/dev-mcp-server/src/index.py"]
    }
  }
}
```

**For Discord-MCP-Server:**
```json
{
  "mcpServers": {
    "discord-mcp-server": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": ["/absolute/path/to/mcp-servers/discord-mcp-server/src/index.py"],
      "env": {
        "DISCORD_TOKEN": "your_bot_token_here"
      }
    }
  }
}
```

### General Installation Steps

1. **Locate IDE Configuration File**
   - Most IDEs store MCP configuration in a settings or config directory
   - Common locations: user settings folder, `.config` directory, or IDE-specific storage
   - The file is typically named `mcp.json`, `mcp_settings.json`, or similar

2. **Edit Configuration**
   - Open the configuration file in a text editor
   - Add your server configuration using the format above
   - Replace placeholder paths with your actual absolute paths
   - Ensure JSON syntax is valid (proper commas, quotes, brackets)

3. **Restart IDE**
   - Close and reopen your IDE completely
   - This allows the IDE to load the new MCP server configuration

4. **Verify Installation**
   - Check IDE logs or status for MCP server connection
   - Look for your server name in IDE's MCP/server list
   - Try using a tool from your server to confirm it's working

### Getting IDE-Specific Help

Since each IDE has different configuration locations and methods:

- **Ask your IDE's AI assistant** for help locating the MCP configuration file
- **Check your IDE's documentation** for MCP server setup instructions
- **Look for MCP settings** in your IDE's preferences/settings menu
- **Search IDE settings** for "MCP" or "Model Context Protocol"

The AI assistant can help you:
- Find the exact configuration file location for your IDE
- Format the configuration correctly for your IDE
- Troubleshoot connection issues
- Verify the server is properly configured

### Common Issues

**Problem**: IDE can't find Python executable
- **Solution**: Use absolute paths, not relative paths
- **Solution**: Verify the Python path exists: `ls /path/to/venv/bin/python` (macOS/Linux) or `dir C:\path\to\venv\Scripts\python.exe` (Windows)

**Problem**: Server doesn't appear in IDE
- **Solution**: Check JSON syntax is valid (use a JSON validator)
- **Solution**: Ensure you restarted the IDE completely
- **Solution**: Check IDE logs for error messages

**Problem**: Server starts but tools don't work
- **Solution**: Verify server works manually first: `python src/index.py`
- **Solution**: Check that all dependencies are installed in the venv
- **Solution**: Review server logs for specific error messages

## Setup Script (Optional)

You can automate setup with a simple script:

```bash
#!/bin/bash
# setup.sh

echo "Setting up MCP-ISO..."

# Setup Dev-MCP-Server
echo "Setting up Dev-MCP-Server..."
cd mcp-servers/dev-mcp-server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ../..

# Setup Discord-MCP-Server
echo "Setting up Discord-MCP-Server..."
cd mcp-servers/discord-mcp-server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ../..

echo "Setup complete!"
echo "Remember to create .env file in discord-mcp-server/ with your Discord credentials"
```

## Troubleshooting

### Virtual Environment Issues

**Problem**: `python -m venv` command not found
**Solution**: Ensure Python 3.10+ is installed and in your PATH

**Problem**: Import errors after installation
**Solution**: 
1. Verify venv is activated: `which python` should show venv path
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Discord-MCP-Server Issues

**Problem**: Discord API calls fail
**Solution**:
1. Verify `.env` file exists in `mcp-servers/discord-mcp-server/`
2. Check token is correct (no extra spaces)
3. Ensure bot is invited to server with required permissions

**Problem**: MCP client can't connect
**Solution**:
1. Use full path to venv Python in MCP client config
2. Verify server starts manually: `python src/index.py`
3. Check for error messages in server output

### General Issues

**Problem**: Permission denied errors
**Solution**: 
- On macOS/Linux: `chmod +x setup.sh` (if using setup script)
- Ensure you have write permissions in the repository directory

**Problem**: Multiple Python versions
**Solution**: Use `python3` instead of `python`, or specify version: `python3.10 -m venv venv`

## Next Steps

After setup:

1. **Test the Server**: Run `python src/index.py` to verify it starts correctly

2. **Install into IDE**: Follow the [Installing MCP Servers into Your IDE](#installing-mcp-servers-into-your-ide) section above to configure your IDE

3. **Read the server README**: Each MCP server has detailed documentation
   - [Dev-MCP-Server README](mcp-servers/dev-mcp-server/README.md)
   - [Discord-MCP-Server README](mcp-servers/discord-mcp-server/README.md)

4. **Explore Tools**: Check available tools in each server's README and try using them through your IDE

## Additional Resources

- [MCP Server Guide](docs/MCP_SERVER_GUIDE.md) - Complete guide to creating MCP servers
- [MCP Best Use Cases](docs/MCP_BEST_USE_CASES.md) - Best practices and patterns
- [MCP Specification](https://modelcontextprotocol.io)
- [Discord Developer Portal](https://discord.com/developers)

