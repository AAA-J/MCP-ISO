# How to Verify MCP Servers Are Running

This guide shows you multiple ways to check if your MCP servers are up and running in Cursor.

## Method 1: Check Cursor's MCP Server Status (Recommended)

### In Cursor IDE:

1. **Open Command Palette** (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux)
2. **Search for "MCP"** - Look for commands like:
   - `MCP: Show Server Status`
   - `MCP: List Servers`
   - `MCP: Restart Server`

3. **Check the Status Bar** - Look at the bottom of Cursor for MCP server indicators

4. **Check Output Panel**:
   - Go to `View` → `Output`
   - Select "MCP" or "Model Context Protocol" from the dropdown
   - Look for connection messages or errors

5. **Check Developer Tools** (if available):
   - `Help` → `Toggle Developer Tools`
   - Look in the Console for MCP-related messages

## Method 2: Use the Check Script (Recommended)

The easiest way to verify your setup is to use the check script:

```bash
./scripts/check_mcp_servers.sh
```

This script will:
- Check your MCP configuration file
- Verify server paths exist
- Check Python versions
- Verify dependencies are installed
- Test server startup

## Method 3: Test Servers Manually from Command Line

Before servers can work in Cursor, they should start without errors manually:

### Test Dev-MCP-Server:

```bash
cd mcp-servers/development/dev-mcp-server
source venv/bin/activate
python src/index.py
```

**Expected behavior**: The server should start and wait for input (it won't show much output in stdio mode, which is normal).

**If you see errors**: 
- Python version issues (needs 3.10+)
- Missing dependencies
- Import errors

### Test Discord-MCP-Server:

```bash
cd mcp-servers/development/discord-mcp-server
source venv/bin/activate
python src/index.py
```

**Expected behavior**: Same as above - server starts and waits.

## Method 4: Check Cursor Logs

Cursor stores logs that can show MCP server connection status:

```bash
# Find the most recent log directory
ls -lt ~/Library/Application\ Support/Cursor/logs/ | head -5

# Check MCP-related logs (replace with your latest log directory)
cat ~/Library/Application\ Support/Cursor/logs/[LATEST_DIR]/window*/exthost/anysphere.cursor-mcp/*.log | grep -i "dev-mcp-server\|discord-mcp-server" | tail -20
```

Look for:
- ✅ Connection success messages
- ❌ Error messages about Python version
- ❌ Import errors
- ❌ Path not found errors

## Method 5: Try Using a Tool from the Server

The best way to verify a server is working is to actually use it:

### For Dev-MCP-Server:

Try asking the AI assistant in Cursor:
- "Use the spec_get_mcp_spec tool to get information about tools"
- "List available tools from dev-mcp-server"
- "Use scaffold_mcp_server to create a new server"

### For Discord-MCP-Server:

Try asking:
- "Use discord_scaffold_app to create a Discord bot"
- "List Discord tools available"

**If tools work**: ✅ Server is running correctly!

**If tools don't appear or fail**: ❌ Check the logs and verify setup

## Method 6: Verify Configuration File

Check that your configuration is correct:

```bash
# View your MCP configuration
cat ~/.cursor/mcp.json | python3 -m json.tool

# Verify paths exist (replace with your actual repository path)
REPO_ROOT="$(pwd)"  # Run from repository root
test -f "$REPO_ROOT/mcp-servers/development/dev-mcp-server/venv/bin/python" && echo "✅ dev-mcp-server Python exists" || echo "❌ dev-mcp-server Python missing"
test -f "$REPO_ROOT/mcp-servers/development/discord-mcp-server/venv/bin/python" && echo "✅ discord-mcp-server Python exists" || echo "❌ discord-mcp-server Python missing"
```

Or use the check script which handles paths automatically:
```bash
./scripts/check_mcp_servers.sh
```

## Common Issues and Solutions

### Issue: Server shows as "disconnected" or doesn't appear

**Solutions**:
1. **Restart Cursor completely** (quit and reopen)
2. **Check Python version** - MCP requires Python 3.10+
   ```bash
   python3 --version  # Should be 3.10 or higher
   ```
3. **Verify dependencies are installed**:
   ```bash
   cd mcp-servers/development/dev-mcp-server
   source venv/bin/activate
   pip list | grep mcp
   ```

### Issue: "Python version not supported" error

**Solution**: Install Python 3.10+ and recreate venvs:
```bash
# Install Python 3.10+ (using Homebrew on macOS)
brew install python@3.10

# Recreate venv with correct Python
cd mcp-servers/development/dev-mcp-server
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Module not found" or import errors

**Solution**: Install dependencies:
```bash
cd mcp-servers/development/dev-mcp-server
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Command not found" or path errors

**Solution**: Verify paths in `~/.cursor/mcp.json` are absolute and correct:
```bash
# Check if paths exist (replace with your actual repository path)
REPO_ROOT="$(pwd)"  # Run from repository root
ls -la "$REPO_ROOT/mcp-servers/development/dev-mcp-server/venv/bin/python"
ls -la "$REPO_ROOT/mcp-servers/development/dev-mcp-server/src/index.py"
```

Or use the check script:
```bash
./scripts/check_mcp_servers.sh
```

## Quick Verification Checklist

- [ ] Configuration file exists at `~/.cursor/mcp.json`
- [ ] JSON syntax is valid (no errors)
- [ ] Python paths in config point to existing files
- [ ] Python version is 3.10+ in venvs
- [ ] Dependencies are installed (`pip list | grep mcp`)
- [ ] Server starts manually without errors
- [ ] Cursor has been restarted after configuration
- [ ] Tools from servers are available in Cursor

## Next Steps

Once servers are verified as running:

1. **Explore available tools** - Check each server's README for tool lists
2. **Test tools** - Try using tools through the AI assistant
3. **Check server logs** - Monitor for any runtime errors
4. **Customize configuration** - Add environment variables if needed (e.g., Discord tokens)

---

**Note**: If you're still having issues after following this guide, check the server-specific README files:
- [Dev-MCP-Server README](mcp-servers/development/dev-mcp-server/README.md)
- [Discord-MCP-Server README](mcp-servers/development/discord-mcp-server/README.md)

