#!/usr/bin/env python3
"""
Test script to demonstrate CLI options
"""

import sys
from pathlib import Path

print("🎯 CLI Interface Options for Redaptive Agentic Platform")
print("=" * 60)

print("\n📱 Option 1: Terminal CLI (with log toggle)")
print("   Run: ./activate_venv.sh python interactive_cli.py")
print("   Features:")
print("   • Type 'logs' to toggle verbose initialization logs")
print("   • Type 'help' for available commands")
print("   • Type 'quit' to exit")
print("   • Natural language prompts")

print("\n🌐 Option 2: Web-based CLI (with expandable sections)")
print("   Run: ./activate_venv.sh python web_cli.py")
print("   Features:")
print("   • Click to expand/collapse log sections")
print("   • Web interface with JSON results")
print("   • Real-time processing")
print("   • Browser-based interaction")

print("\n💡 Recommendation:")
print("   • Use Terminal CLI for quick testing and development")
print("   • Use Web CLI for presentations and detailed analysis")

print("\n🚀 To start:")
print("   Terminal CLI: ./activate_venv.sh python interactive_cli.py")
print("   Web CLI: ./activate_venv.sh python web_cli.py")
print("   Then open: http://localhost:5000") 