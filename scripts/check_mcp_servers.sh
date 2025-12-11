#!/bin/bash
# Quick script to verify MCP servers are set up correctly

# Get the repository root directory (parent of scripts directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 Checking MCP Server Configuration..."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check configuration file
echo "1. Checking MCP configuration file..."
if [ -f ~/.cursor/mcp.json ]; then
    echo -e "${GREEN}✅${NC} Configuration file exists: ~/.cursor/mcp.json"
    
    # Validate JSON
    if python3 -m json.tool ~/.cursor/mcp.json > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} JSON syntax is valid"
    else
        echo -e "${RED}❌${NC} JSON syntax is invalid"
    fi
    
    # Check if our servers are in config
    if grep -q "dev-mcp-server" ~/.cursor/mcp.json; then
        echo -e "${GREEN}✅${NC} dev-mcp-server found in config"
    else
        echo -e "${RED}❌${NC} dev-mcp-server NOT found in config"
    fi
    
    if grep -q "discord-mcp-server" ~/.cursor/mcp.json; then
        echo -e "${GREEN}✅${NC} discord-mcp-server found in config"
    else
        echo -e "${RED}❌${NC} discord-mcp-server NOT found in config"
    fi
else
    echo -e "${RED}❌${NC} Configuration file not found: ~/.cursor/mcp.json"
fi

echo ""
echo "2. Checking server paths..."

# Check dev-mcp-server
DEV_PYTHON="$REPO_ROOT/mcp-servers/development/dev-mcp-server/venv/bin/python"
DEV_SCRIPT="$REPO_ROOT/mcp-servers/development/dev-mcp-server/src/index.py"

if [ -f "$DEV_PYTHON" ]; then
    echo -e "${GREEN}✅${NC} dev-mcp-server Python exists: $DEV_PYTHON"
    PYTHON_VERSION=$($DEV_PYTHON --version 2>&1)
    echo "   Python version: $PYTHON_VERSION"
    
    # Check if Python 3.10+
    MAJOR=$(echo $PYTHON_VERSION | cut -d' ' -f2 | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d' ' -f2 | cut -d'.' -f2)
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]; then
        echo -e "${GREEN}✅${NC} Python version is 3.10+ (required for MCP)"
    else
        echo -e "${RED}❌${NC} Python version is too old (need 3.10+, have $MAJOR.$MINOR)"
    fi
else
    echo -e "${RED}❌${NC} dev-mcp-server Python NOT found: $DEV_PYTHON"
fi

if [ -f "$DEV_SCRIPT" ]; then
    echo -e "${GREEN}✅${NC} dev-mcp-server script exists: $DEV_SCRIPT"
else
    echo -e "${RED}❌${NC} dev-mcp-server script NOT found: $DEV_SCRIPT"
fi

# Check discord-mcp-server
DISCORD_PYTHON="$REPO_ROOT/mcp-servers/development/discord-mcp-server/venv/bin/python"
DISCORD_SCRIPT="$REPO_ROOT/mcp-servers/development/discord-mcp-server/src/index.py"

if [ -f "$DISCORD_PYTHON" ]; then
    echo -e "${GREEN}✅${NC} discord-mcp-server Python exists: $DISCORD_PYTHON"
    PYTHON_VERSION=$($DISCORD_PYTHON --version 2>&1)
    echo "   Python version: $PYTHON_VERSION"
    
    # Check if Python 3.10+
    MAJOR=$(echo $PYTHON_VERSION | cut -d' ' -f2 | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d' ' -f2 | cut -d'.' -f2)
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]; then
        echo -e "${GREEN}✅${NC} Python version is 3.10+ (required for MCP)"
    else
        echo -e "${RED}❌${NC} Python version is too old (need 3.10+, have $MAJOR.$MINOR)"
    fi
else
    echo -e "${RED}❌${NC} discord-mcp-server Python NOT found: $DISCORD_PYTHON"
fi

if [ -f "$DISCORD_SCRIPT" ]; then
    echo -e "${GREEN}✅${NC} discord-mcp-server script exists: $DISCORD_SCRIPT"
else
    echo -e "${RED}❌${NC} discord-mcp-server script NOT found: $DISCORD_SCRIPT"
fi

echo ""
echo "3. Checking dependencies..."

# Check if MCP is installed in dev-mcp-server venv
if [ -f "$DEV_PYTHON" ]; then
    if $DEV_PYTHON -c "import mcp" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} MCP package installed in dev-mcp-server venv"
    else
        echo -e "${RED}❌${NC} MCP package NOT installed in dev-mcp-server venv"
        echo -e "${YELLOW}   Run: cd mcp-servers/development/dev-mcp-server && source venv/bin/activate && pip install -r requirements.txt${NC}"
    fi
fi

# Check if MCP is installed in discord-mcp-server venv
if [ -f "$DISCORD_PYTHON" ]; then
    if $DISCORD_PYTHON -c "import mcp" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} MCP package installed in discord-mcp-server venv"
    else
        echo -e "${RED}❌${NC} MCP package NOT installed in discord-mcp-server venv"
        echo -e "${YELLOW}   Run: cd mcp-servers/development/discord-mcp-server && source venv/bin/activate && pip install -r requirements.txt${NC}"
    fi
fi

echo ""
echo "4. Quick test (server should start without errors)..."
echo ""

# Test dev-mcp-server startup (timeout after 2 seconds)
if [ -f "$DEV_PYTHON" ] && [ -f "$DEV_SCRIPT" ]; then
    echo "Testing dev-mcp-server startup..."
    timeout 2 $DEV_PYTHON "$DEV_SCRIPT" 2>&1 | head -5
    if [ ${PIPESTATUS[0]} -eq 124 ] || [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✅${NC} dev-mcp-server starts without immediate errors"
    else
        echo -e "${RED}❌${NC} dev-mcp-server has startup errors (check output above)"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Summary:"
echo ""
echo "To verify servers are running in Cursor:"
echo "  1. Restart Cursor completely (quit and reopen)"
echo "  2. Check Cursor's Output panel (View → Output → select 'MCP')"
echo "  3. Try using a tool: Ask the AI assistant to use a tool from dev-mcp-server"
echo "  4. Check logs: ~/Library/Application Support/Cursor/logs/"
echo ""
echo "For detailed instructions, see: $REPO_ROOT/VERIFY_MCP_SERVERS.md"
echo ""

