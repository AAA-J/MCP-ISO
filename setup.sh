#!/bin/bash
# MCP-ISO Setup Script
# Automates setup of all MCP servers

set -e  # Exit on error

echo "🚀 Setting up MCP-ISO..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Function to setup a server
setup_server() {
    local category=$1
    local server_name=$2
    local server_path="mcp-servers/$category/$server_name"
    
    echo ""
    echo "📦 Setting up $server_name..."
    
    if [ ! -d "$server_path" ]; then
        echo "⚠️  Directory $server_path not found, skipping..."
        return
    fi
    
    cd "$server_path"
    
    # Create venv if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "  Creating virtual environment..."
        python3 -m venv venv
    else
        echo "  Virtual environment already exists"
    fi
    
    # Activate venv and install dependencies
    echo "  Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    deactivate
    
    cd ../../..
    echo "✓ $server_name setup complete"
}

# Setup Development Tools
echo "📦 Setting up development tools..."
setup_server "development" "dev-mcp-server"
setup_server "development" "discord-mcp-server"

# Setup Application Servers
echo ""
echo "📦 Setting up application servers..."
setup_server "application" "app-docs"
setup_server "application" "app-db-readonly"
setup_server "application" "app-api"
setup_server "application" "app-ops"
setup_server "application" "app-domain"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. For Discord-MCP-Server: Create .env file with Discord credentials"
echo "   2. For custom servers: Configure environment variables in ~/.cursor/mcp.json"
echo "   3. Read SETUP.md for detailed configuration instructions"
echo "   4. Check each server's README for usage examples"
echo ""
echo "📚 Documentation:"
echo "   - Setup Guide: SETUP.md"
echo "   - Dev-MCP-Server: mcp-servers/development/dev-mcp-server/README.md"
echo "   - Discord-MCP-Server: mcp-servers/development/discord-mcp-server/README.md"
echo "   - Application Servers: See mcp-servers/application/app-*/README.md files"

