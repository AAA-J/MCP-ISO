#!/bin/bash
# Setup MCP servers for current project
# Copy this script to your project root and run it

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get current project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"
MCP_JSON="$HOME/.cursor/mcp.json"
MCP_SERVERS_BASE="/Users/aaa-j/Documents/GitHub/MCP-ISO/mcp-servers"

echo -e "${BLUE}Setting up MCP servers for project: ${GREEN}$PROJECT_NAME${NC}"
echo -e "${BLUE}Project directory: ${GREEN}$PROJECT_DIR${NC}\n"

# Check if mcp.json exists
if [ ! -f "$MCP_JSON" ]; then
    echo -e "${RED}Error: $MCP_JSON not found!${NC}"
    exit 1
fi

# Backup mcp.json
cp "$MCP_JSON" "$MCP_JSON.backup.$(date +%Y%m%d_%H%M%S)"
echo -e "${YELLOW}Backed up mcp.json${NC}\n"

# Auto-detect project configuration
echo -e "${BLUE}Auto-detecting project configuration...${NC}"

# Detect docs directory
DOCS_DIR="docs"
if [ -d "$PROJECT_DIR/docs" ]; then
    DOCS_DIR="docs"
elif [ -d "$PROJECT_DIR/documentation" ]; then
    DOCS_DIR="documentation"
elif [ -d "$PROJECT_DIR/doc" ]; then
    DOCS_DIR="doc"
else
    echo -e "${YELLOW}  No docs directory found, using 'docs' as default${NC}"
fi

# Detect database type (look for common config files)
DB_TYPE="azure_sql"
if [ -f "$PROJECT_DIR/.env" ] || [ -f "$PROJECT_DIR/.env.local" ]; then
    # Try to detect from .env file
    if grep -q "POSTGRES" "$PROJECT_DIR/.env" 2>/dev/null; then
        DB_TYPE="postgresql"
    elif grep -q "MYSQL" "$PROJECT_DIR/.env" 2>/dev/null; then
        DB_TYPE="mysql"
    fi
fi

# Detect API type (look for framework files)
API_TYPE="rest"
if [ -f "$PROJECT_DIR/requirements.txt" ] && grep -q "fastapi\|flask" "$PROJECT_DIR/requirements.txt" 2>/dev/null; then
    API_TYPE="fastapi"
elif [ -f "$PROJECT_DIR/package.json" ] && grep -q "express" "$PROJECT_DIR/package.json" 2>/dev/null; then
    API_TYPE="express"
elif [ -f "$PROJECT_DIR/schema.graphql" ] || [ -f "$PROJECT_DIR/src/schema.graphql" ]; then
    API_TYPE="graphql"
fi

# Detect API port (common defaults)
API_PORT="8000"
if [ -f "$PROJECT_DIR/.env" ]; then
    DETECTED_PORT=$(grep -E "PORT|API_PORT|SERVER_PORT" "$PROJECT_DIR/.env" 2>/dev/null | head -1 | cut -d'=' -f2 | tr -d ' ' || echo "")
    if [ ! -z "$DETECTED_PORT" ]; then
        API_PORT="$DETECTED_PORT"
    fi
fi

# Detect GitHub repo (if .git exists)
GITHUB_OWNER=""
GITHUB_REPO=""
if [ -d "$PROJECT_DIR/.git" ]; then
    REMOTE_URL=$(git -C "$PROJECT_DIR" remote get-url origin 2>/dev/null || echo "")
    if [[ "$REMOTE_URL" =~ github.com[:/]([^/]+)/([^/]+) ]]; then
        GITHUB_OWNER="${BASH_REMATCH[1]}"
        GITHUB_REPO="${BASH_REMATCH[2]%.git}"
    fi
fi

echo -e "${GREEN}  Detected configuration:${NC}"
echo -e "    Docs directory: $DOCS_DIR"
echo -e "    Database type: $DB_TYPE"
echo -e "    API type: $API_TYPE"
echo -e "    API port: $API_PORT"
if [ ! -z "$GITHUB_OWNER" ]; then
    echo -e "    GitHub: $GITHUB_OWNER/$GITHUB_REPO"
fi
echo ""

# Read current mcp.json
MCP_CONTENT=$(cat "$MCP_JSON")

# Function to update or add server config
update_server_config() {
    local server_name=$1
    local env_vars=$2
    
    # Check if server already exists
    if echo "$MCP_CONTENT" | grep -q "\"$server_name\""; then
        echo -e "${YELLOW}  Updating existing $server_name configuration...${NC}"
        # Use Python to update JSON (more reliable than sed)
        python3 << EOF
import json
import sys

with open("$MCP_JSON", 'r') as f:
    config = json.load(f)

if "$server_name" in config.get("mcpServers", {}):
    # Update existing
    config["mcpServers"]["$server_name"]["env"].update($env_vars)
else:
    # Add new
    config.setdefault("mcpServers", {})["$server_name"] = {
        "command": "$MCP_SERVERS_BASE/$server_name/venv/bin/python",
        "args": ["$MCP_SERVERS_BASE/$server_name/src/index.py"],
        "env": $env_vars
    }

with open("$MCP_JSON", 'w') as f:
    json.dump(config, f, indent=2)
EOF
    else
        echo -e "${GREEN}  Adding $server_name configuration...${NC}"
        python3 << EOF
import json

with open("$MCP_JSON", 'r') as f:
    config = json.load(f)

config.setdefault("mcpServers", {})["$server_name"] = {
    "command": "$MCP_SERVERS_BASE/$server_name/venv/bin/python",
    "args": ["$MCP_SERVERS_BASE/$server_name/src/index.py"],
    "env": $env_vars
}

with open("$MCP_JSON", 'w') as f:
    json.dump(config, f, indent=2)
EOF
    fi
    
    # Reload content
    MCP_CONTENT=$(cat "$MCP_JSON")
}

# Update app-docs
echo -e "${BLUE}Configuring app-docs...${NC}"
update_server_config "app-docs" "{\"BASE_DIR\": \"$PROJECT_DIR\", \"DOCS_DIR\": \"$DOCS_DIR\"}"

# Update app-db-readonly (keep existing connection string if present)
echo -e "${BLUE}Configuring app-db-readonly...${NC}"
# Try to extract existing connection string
EXISTING_DB_CONN=$(echo "$MCP_CONTENT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('mcpServers', {}).get('app-db-readonly', {}).get('env', {}).get('DB_CONNECTION_STRING', ''))" 2>/dev/null || echo "")
if [ -z "$EXISTING_DB_CONN" ]; then
    # Prompt for connection string or use default
    echo -e "${YELLOW}  No existing DB connection found.${NC}"
    echo -e "${YELLOW}  You may need to manually set DB_CONNECTION_STRING in mcp.json${NC}"
    EXISTING_DB_CONN=""
fi
update_server_config "app-db-readonly" "{\"DB_TYPE\": \"$DB_TYPE\", \"DB_CONNECTION_STRING\": \"$EXISTING_DB_CONN\"}"

# Update app-api
echo -e "${BLUE}Configuring app-api...${NC}"
API_BASE_URL="http://localhost:$API_PORT"
EXISTING_AUTH_TOKEN=$(echo "$MCP_CONTENT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('mcpServers', {}).get('app-api', {}).get('env', {}).get('AUTH_TOKEN', ''))" 2>/dev/null || echo "")
update_server_config "app-api" "{\"API_BASE_URL\": \"$API_BASE_URL\", \"API_TYPE\": \"$API_TYPE\", \"AUTH_TYPE\": \"bearer\", \"AUTH_TOKEN\": \"$EXISTING_AUTH_TOKEN\"}"

# Update app-ops (if GitHub repo detected)
if [ ! -z "$GITHUB_OWNER" ] && [ ! -z "$GITHUB_REPO" ]; then
    echo -e "${BLUE}Configuring app-ops...${NC}"
    EXISTING_CICD_TOKEN=$(echo "$MCP_CONTENT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('mcpServers', {}).get('app-ops', {}).get('env', {}).get('CICD_TOKEN', ''))" 2>/dev/null || echo "")
    update_server_config "app-ops" "{\"CICD_TYPE\": \"github_actions\", \"CICD_TOKEN\": \"$EXISTING_CICD_TOKEN\", \"CICD_OWNER\": \"$GITHUB_OWNER\", \"CICD_REPO\": \"$GITHUB_REPO\"}"
else
    echo -e "${YELLOW}Skipping app-ops (no GitHub repo detected)${NC}"
fi

# Update app-domain
echo -e "${BLUE}Configuring app-domain...${NC}"
DOMAIN_TOOLS_CONFIG="$MCP_SERVERS_BASE/app-domain/domain_tools.yaml"
EXISTING_DOMAIN_AUTH=$(echo "$MCP_CONTENT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('mcpServers', {}).get('app-domain', {}).get('env', {}).get('AUTH_TOKEN', ''))" 2>/dev/null || echo "")
update_server_config "app-domain" "{\"DOMAIN_TOOLS_CONFIG\": \"$DOMAIN_TOOLS_CONFIG\", \"API_BASE_URL\": \"$API_BASE_URL\", \"AUTH_TYPE\": \"bearer\", \"AUTH_TOKEN\": \"$EXISTING_DOMAIN_AUTH\"}"

echo -e "\n${GREEN}✓ MCP configuration updated!${NC}"
echo -e "\n${BLUE}Next steps:${NC}"
echo -e "1. Review and update $MCP_JSON if needed"
echo -e "2. Set any missing values (DB_CONNECTION_STRING, AUTH_TOKEN, etc.)"
echo -e "3. Restart Cursor to load the updated configuration"
echo -e "\n${YELLOW}Note: Your original mcp.json was backed up${NC}"

