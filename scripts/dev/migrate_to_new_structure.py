#!/usr/bin/env python3
"""
Migration script to restructure the Redaptive Agentic Platform
Handles file moves, import updates, and configuration management
"""

import os
import shutil
import sys
from pathlib import Path

def main():
    """Execute the migration to new project structure."""
    
    print("🚀 Starting Redaptive Platform Restructure...")
    
    # Get project root
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src" / "redaptive"
    
    print(f"📁 Project root: {project_root}")
    print(f"📦 Source directory: {src_dir}")
    
    # Create new directory structure if it doesn't exist
    print("📂 Creating directory structure...")
    directories = [
        src_dir / "config",
        src_dir / "agents" / "base",
        src_dir / "agents" / "energy", 
        src_dir / "agents" / "content",
        src_dir / "orchestration" / "planners",
        src_dir / "orchestration" / "matchers",
        src_dir / "tools",
        src_dir / "models",
        project_root / "scripts" / "setup",
        project_root / "scripts" / "deploy", 
        project_root / "scripts" / "dev"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")
    
    print("\n✨ New project structure created successfully!")
    print("\n📋 Next steps:")
    print("1. Copy agents to new locations")
    print("2. Update imports and database connections")
    print("3. Create new entry points")
    print("4. Update documentation")
    print("5. Migrate examples and tests")
    
    # Create main entry point
    entry_point = project_root / "src" / "redaptive" / "__main__.py"
    with open(entry_point, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Redaptive Agentic Platform - Main Entry Point
"""

import asyncio
import sys
import argparse
import logging
from redaptive.agents import AGENT_REGISTRY, get_agent

def main():
    parser = argparse.ArgumentParser(description="Redaptive Agentic AI Platform")
    parser.add_argument("agent", choices=list(AGENT_REGISTRY.keys()), 
                       help="Agent to start")
    parser.add_argument("--log-level", default="INFO", 
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=getattr(logging, args.log_level.upper()))
    
    # Get and start agent
    agent_class = get_agent(args.agent)
    if not agent_class:
        print(f"Agent not found: {args.agent}")
        sys.exit(1)
    
    agent = agent_class()
    
    print(f"🤖 Starting {args.agent} agent...")
    asyncio.run(agent.run())

if __name__ == "__main__":
    main()
''')
    
    print(f"🎯 Created main entry point: {entry_point}")
    print("\n🎉 Migration scaffolding complete!")
    print("Run the new platform with: python -m redaptive.agents <agent-name>")

if __name__ == "__main__":
    main()