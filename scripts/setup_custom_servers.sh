#!/bin/bash
# Setup script for custom MCP servers (app-docs, app-db-readonly, app-api, app-ops, app-domain)

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MCP_SERVERS_DIR="$REPO_ROOT/mcp-servers/application"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up custom MCP servers...${NC}\n"

# Array of server names
SERVERS=("app-docs" "app-db-readonly" "app-api" "app-ops" "app-domain")

# Function to setup a single server
setup_server() {
    local server_name=$1
    local server_dir="$MCP_SERVERS_DIR/$server_name"
    
    echo -e "${BLUE}Setting up $server_name...${NC}"
    
    if [ ! -d "$server_dir" ]; then
        echo -e "${RED}Error: Directory $server_dir does not exist!${NC}"
        return 1
    fi
    
    cd "$server_dir"
    
    # Use the same Python as existing servers (Python 3.13)
    PYTHON_CMD=""
    if [ -f "$REPO_ROOT/mcp-servers/development/dev-mcp-server/venv/bin/python" ]; then
        # Use the same Python interpreter as existing servers
        PYTHON_CMD="$REPO_ROOT/mcp-servers/development/dev-mcp-server/venv/bin/python"
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
        echo -e "  ${YELLOW}Using $PYTHON_VERSION from existing server${NC}"
    else
        # Fallback to system Python versions
        if command -v python3.13 &> /dev/null; then
            PYTHON_CMD="python3.13"
        elif command -v python3.12 &> /dev/null; then
            PYTHON_CMD="python3.12"
        elif command -v python3.11 &> /dev/null; then
            PYTHON_CMD="python3.11"
        elif command -v python3.10 &> /dev/null; then
            PYTHON_CMD="python3.10"
        else
            echo -e "  ${RED}Error: Python 3.10+ is required but not found${NC}"
            return 1
        fi
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo -e "  ${YELLOW}Creating virtual environment with $PYTHON_CMD ($PYTHON_VERSION)...${NC}"
        $PYTHON_CMD -m venv venv
    else
        echo -e "  ${YELLOW}Virtual environment already exists, skipping...${NC}"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    echo -e "  ${YELLOW}Upgrading pip...${NC}"
    pip install --upgrade pip --quiet
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        echo -e "  ${YELLOW}Installing requirements...${NC}"
        pip install -r requirements.txt --quiet
        echo -e "  ${GREEN}✓ $server_name setup complete!${NC}\n"
    else
        echo -e "  ${YELLOW}Warning: requirements.txt not found, skipping installation${NC}\n"
    fi
    
    # Deactivate virtual environment
    deactivate
    
    return 0
}

# Setup each server
for server in "${SERVERS[@]}"; do
    setup_server "$server"
done

echo -e "${GREEN}All custom MCP servers have been set up!${NC}\n"

# Verify setup
echo -e "${BLUE}Verifying setup...${NC}\n"
for server in "${SERVERS[@]}"; do
    server_dir="$MCP_SERVERS_DIR/$server"
    if [ -d "$server_dir/venv" ] && [ -f "$server_dir/src/index.py" ]; then
        echo -e "  ${GREEN}✓ $server${NC}"
    else
        echo -e "  ${RED}✗ $server (missing venv or index.py)${NC}"
    fi
done

echo -e "\n${BLUE}Next steps:${NC}"
echo -e "1. Update environment variables in ~/.cursor/mcp.json"
echo -e "2. Restart Cursor to load the new MCP servers"
echo -e "3. Test each server to ensure it's working correctly"
echo -e "\n${YELLOW}Note: Make sure to configure the following:${NC}"
echo -e "  - app-docs: Set BASE_DIR and DOCS_DIR if needed"
echo -e "  - app-db-readonly: Set DB_CONNECTION_STRING"
echo -e "  - app-api: Set API_BASE_URL and AUTH_TOKEN"
echo -e "  - app-ops: Set CICD_OWNER and CICD_REPO"
echo -e "  - app-domain: Configure domain_tools.yaml"

