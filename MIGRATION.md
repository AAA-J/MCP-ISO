# Migration Guide: Repository Reorganization

This guide helps you update your configuration after the MCP-ISO repository reorganization.

## What Changed?

The MCP servers have been reorganized into two categories:

### Before
```
mcp-servers/
├── dev-mcp-server/
├── discord-mcp-server/
├── app-docs/
├── app-db-readonly/
├── app-api/
├── app-ops/
└── app-domain/
```

### After
```
mcp-servers/
├── development/
│   ├── dev-mcp-server/
│   └── discord-mcp-server/
└── application/
    ├── app-docs/
    ├── app-db-readonly/
    ├── app-api/
    ├── app-ops/
    └── app-domain/
```

## What You Need to Update

### 1. MCP Configuration File

Update your IDE's MCP configuration file (typically `~/.cursor/mcp.json` or similar).

#### Development Tools

**Before:**
```json
{
  "mcpServers": {
    "dev-mcp-server": {
      "command": "/path/to/mcp-servers/dev-mcp-server/venv/bin/python",
      "args": ["/path/to/mcp-servers/dev-mcp-server/src/index.py"]
    }
  }
}
```

**After:**
```json
{
  "mcpServers": {
    "dev-mcp-server": {
      "command": "/path/to/mcp-servers/development/dev-mcp-server/venv/bin/python",
      "args": ["/path/to/mcp-servers/development/dev-mcp-server/src/index.py"]
    }
  }
}
```

#### Application Servers

**Before:**
```json
{
  "mcpServers": {
    "app-docs": {
      "command": "/path/to/mcp-servers/app-docs/venv/bin/python",
      "args": ["/path/to/mcp-servers/app-docs/src/index.py"]
    }
  }
}
```

**After:**
```json
{
  "mcpServers": {
    "app-docs": {
      "command": "/path/to/mcp-servers/application/app-docs/venv/bin/python",
      "args": ["/path/to/mcp-servers/application/app-docs/src/index.py"]
    }
  }
}
```

### 2. Path Updates Summary

| Server | Old Path | New Path |
|--------|----------|----------|
| dev-mcp-server | `mcp-servers/dev-mcp-server/` | `mcp-servers/development/dev-mcp-server/` |
| discord-mcp-server | `mcp-servers/discord-mcp-server/` | `mcp-servers/development/discord-mcp-server/` |
| app-docs | `mcp-servers/app-docs/` | `mcp-servers/application/app-docs/` |
| app-db-readonly | `mcp-servers/app-db-readonly/` | `mcp-servers/application/app-db-readonly/` |
| app-api | `mcp-servers/app-api/` | `mcp-servers/application/app-api/` |
| app-ops | `mcp-servers/app-ops/` | `mcp-servers/application/app-ops/` |
| app-domain | `mcp-servers/app-domain/` | `mcp-servers/application/app-domain/` |

### 3. Environment Variables

If you have any environment variables or configuration files that reference the old paths, update them:

- `.env` files in server directories (paths are relative, so no change needed)
- Scripts that reference server paths
- CI/CD configurations
- Documentation references

### 4. Scripts and Automation

If you have custom scripts that reference server paths, update them:

**Before:**
```bash
cd mcp-servers/dev-mcp-server
```

**After:**
```bash
cd mcp-servers/development/dev-mcp-server
```

## Quick Migration Script

If you need to update multiple configuration files, you can use this pattern:

```bash
# Update MCP configuration file
sed -i '' 's|mcp-servers/dev-mcp-server|mcp-servers/development/dev-mcp-server|g' ~/.cursor/mcp.json
sed -i '' 's|mcp-servers/discord-mcp-server|mcp-servers/development/discord-mcp-server|g' ~/.cursor/mcp.json
sed -i '' 's|mcp-servers/app-|mcp-servers/application/app-|g' ~/.cursor/mcp.json
```

**Note:** Test the script on a backup first, and adjust the path to your MCP configuration file.

## Verification

After updating your configuration:

1. **Restart your IDE** completely (quit and reopen)
2. **Check server status** - Verify servers are connected
3. **Test a tool** - Try using a tool from one of the servers
4. **Run verification script**:
   ```bash
   ./scripts/check_mcp_servers.sh
   ```

## Benefits of the New Structure

- **Clearer organization** - Development tools vs. application servers
- **Better discoverability** - Easier to find servers by purpose
- **Scalability** - Easier to add new servers in appropriate categories
- **Documentation** - Category-specific README files explain each group

## Need Help?

- Check [SETUP.md](SETUP.md) for updated setup instructions
- See [VERIFY_MCP_SERVERS.md](VERIFY_MCP_SERVERS.md) for verification steps
- Review individual server READMEs in their new locations

## Rollback

If you need to rollback, you can move servers back to the root `mcp-servers/` directory, but you'll need to update all documentation and scripts accordingly. The new structure is recommended for better organization.

