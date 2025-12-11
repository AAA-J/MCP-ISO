# Project MCP Setup Script

This script automatically configures the SaaS MCP servers for any project you're working on.

## Quick Start

1. **Copy the script to your project root:**
   ```bash
   cp /Users/aaa-j/Documents/GitHub/MCP-ISO/setup-project-mcp.sh /path/to/your/project/
   ```

2. **Run it:**
   ```bash
   cd /path/to/your/project
   ./setup-project-mcp.sh
   ```

3. **Done!** The script will:
   - Auto-detect your project configuration
   - Update your `~/.cursor/mcp.json` with project-specific settings
   - Preserve existing tokens and connection strings
   - Create a backup of your mcp.json

## What It Auto-Detects

### Project Structure
- **Docs directory**: Looks for `docs/`, `documentation/`, or `doc/`
- **Project path**: Uses the directory where you run the script

### Database Type
- Checks `.env` files for database indicators
- Defaults to `azure_sql` if not detected

### API Configuration
- **Framework**: Detects FastAPI, Flask, Express, or GraphQL
- **Port**: Reads from `.env` file (PORT, API_PORT, SERVER_PORT)
- **Type**: Auto-detects REST, GraphQL, FastAPI, or Express

### GitHub Integration
- **Repository**: Auto-detects from `.git` remote URL
- **Owner/Repo**: Extracts from GitHub URL

## What Gets Updated

### app-docs
- `BASE_DIR`: Set to your project directory
- `DOCS_DIR`: Auto-detected docs folder

### app-db-readonly
- `DB_TYPE`: Auto-detected or defaults to azure_sql
- `DB_CONNECTION_STRING`: Preserved from existing config (if present)

### app-api
- `API_BASE_URL`: Set to `http://localhost:{detected_port}`
- `API_TYPE`: Auto-detected framework type
- `AUTH_TOKEN`: Preserved from existing config (if present)

### app-ops
- `CICD_OWNER`: Auto-detected from Git remote
- `CICD_REPO`: Auto-detected from Git remote
- `CICD_TOKEN`: Preserved from existing config (if present)

### app-domain
- `DOMAIN_TOOLS_CONFIG`: Set to default location
- `API_BASE_URL`: Uses same as app-api
- `AUTH_TOKEN`: Preserved from existing config (if present)

## Manual Overrides

After running the script, you can manually edit `~/.cursor/mcp.json` to:
- Update connection strings
- Add authentication tokens
- Adjust API URLs
- Configure observability endpoints

## Examples

### Example 1: FastAPI Project
```bash
cd ~/projects/my-fastapi-app
./setup-project-mcp.sh
# Detects: FastAPI, port 8000, docs/ directory
```

### Example 2: Express.js Project
```bash
cd ~/projects/my-express-app
./setup-project-mcp.sh
# Detects: Express, port 3000, documentation/ directory
```

### Example 3: Project with Custom Config
```bash
cd ~/projects/my-custom-app
./setup-project-mcp.sh
# Auto-detects what it can, you manually update the rest
```

## Backup

The script automatically creates a backup of your `mcp.json`:
- Location: `~/.cursor/mcp.json.backup.YYYYMMDD_HHMMSS`
- You can restore from backup if needed

## Troubleshooting

**Script not found:**
- Make sure you copied it to your project directory
- Or use the full path: `/Users/aaa-j/Documents/GitHub/MCP-ISO/setup-project-mcp.sh`

**Python errors:**
- Requires Python 3 (for JSON manipulation)
- Should be available on macOS by default

**GitHub not detected:**
- Make sure your project has a `.git` directory
- Ensure `origin` remote is set: `git remote add origin <url>`

**Missing values:**
- The script preserves existing tokens/connection strings
- If missing, you'll need to add them manually to `mcp.json`

## Tips

1. **Run once per project**: The script is idempotent - safe to run multiple times
2. **Keep tokens secure**: The script preserves existing tokens, but be careful with backups
3. **Customize after**: Run the script first, then customize specific values in `mcp.json`
4. **Multiple projects**: The script updates the same `mcp.json`, so it switches between projects

