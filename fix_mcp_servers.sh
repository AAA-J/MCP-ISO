#!/bin/bash
# Script to fix MCP servers by installing Python 3.10+ and setting up venvs correctly

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔧 Fixing MCP Servers Setup"
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo -e "${RED}❌${NC} Homebrew is not installed."
    echo "Please install Homebrew first: https://brew.sh"
    exit 1
fi

# Find Python 3.10+
PYTHON_CMD=""
for version in python3.13 python3.12 python3.11 python3.10; do
    if command -v $version &> /dev/null; then
        PYTHON_VERSION=$($version --version 2>&1 | cut -d' ' -f2)
        MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON_CMD=$version
            echo -e "${GREEN}✅${NC} Found Python $PYTHON_VERSION"
            break
        fi
    fi
done

# Install Python 3.10+ if not found
if [ -z "$PYTHON_CMD" ]; then
    echo -e "${YELLOW}⚠️${NC} Python 3.10+ not found. Installing Python 3.11 via Homebrew..."
    brew install python@3.11
    
    # Try to find it after installation
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
        echo -e "${GREEN}✅${NC} Python 3.11 installed successfully"
    else
        echo -e "${RED}❌${NC} Failed to install Python 3.11"
        echo "Please install Python 3.10+ manually and run this script again"
        exit 1
    fi
fi

echo ""
echo "Setting up dev-mcp-server..."
cd "$(dirname "$0")/mcp-servers/dev-mcp-server"

# Remove old venv
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create new venv with Python 3.10+
echo "Creating virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

# Activate and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

echo -e "${GREEN}✅${NC} dev-mcp-server setup complete"
deactivate

echo ""
echo "Setting up discord-mcp-server..."
cd "../discord-mcp-server"

# Remove old venv
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create new venv with Python 3.10+
echo "Creating virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

# Activate and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

echo -e "${GREEN}✅${NC} discord-mcp-server setup complete"
deactivate

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✅${NC} Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Restart Cursor completely (quit and reopen)"
echo "  2. The MCP servers should now show as connected (green status)"
echo "  3. Try using a tool from one of the servers to verify"
echo ""
echo "If you still see errors, check:"
echo "  - Cursor's Output panel (View → Output → select 'MCP')"
echo "  - Run: ./check_mcp_servers.sh"
echo ""

