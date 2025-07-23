#!/bin/bash

# Activate virtual environment and run commands
# Usage: ./activate_venv.sh [command]
# Example: ./activate_venv.sh python scripts/mcp/configure.sh

if [ -z "$1" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated!"
    echo "💡 You can now run commands like:"
    echo "   python scripts/mcp/configure.sh"
    echo "   python scripts/mcp/working_mcp_client.py"
    echo "   python -m pytest tests/"
    echo ""
    echo "🔧 To deactivate, run: deactivate"
else
    echo "🔧 Running command with virtual environment: $1"
    source venv/bin/activate && $@
fi 