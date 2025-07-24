#!/usr/bin/env python3
"""
Cursor IDE MCP Configuration Generator

Generates MCP server configuration specifically for Cursor IDE integration.
Creates .cursor/mcp.json with proper paths and environment variables.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

def generate_cursor_mcp_config():
    """Generate MCP configuration for Cursor IDE"""
    
    # Get the absolute path of the project's root directory
    project_root = Path(__file__).parent.parent.parent.absolute()
    
    # Load environment variables from .env file in the project root
    dotenv_path = project_root / '.env'
    load_dotenv(dotenv_path=dotenv_path)
    
    # Path to the cursor mcp.json file
    cursor_dir = project_root / '.cursor'
    cursor_dir.mkdir(exist_ok=True)
    config_path = cursor_dir / 'mcp.json'
    
    # Define the MCP configuration structure for Cursor IDE
    mcp_config = {
        "mcpServers": {
            "redaptive-orchestrator": {
                "command": "python",
                "args": [str(project_root / "orchestration" / "intelligent_orchestrator.py")],
                "description": "Redaptive Intelligent Multi-Agent Orchestrator - Natural language energy management",
                "env": {
                    "POSTGRES_HOST": os.getenv('POSTGRES_HOST', 'localhost'),
                    "POSTGRES_PORT": os.getenv('POSTGRES_PORT', '5432'),
                    "POSTGRES_DATABASE": os.getenv('POSTGRES_DATABASE', 'energy_db'),
                    "POSTGRES_USER": os.getenv('POSTGRES_USER', 'energy_user'),
                    "POSTGRES_PASSWORD": os.getenv('POSTGRES_PASSWORD', 'energy123'),
                    "DB_USER_ENERGY": os.getenv('DB_USER_ENERGY', 'energy_user'),
                    "DB_USERPASSWORD_ENERGY": os.getenv('DB_USERPASSWORD_ENERGY', 'energy123'),
                    "GOOGLE_API_KEY": os.getenv('GOOGLE_API_KEY', ''),
                    "AWS_ACCESS_KEY_ID": os.getenv('AWS_ACCESS_KEY_ID', ''),
                    "AWS_SECRET_ACCESS_KEY": os.getenv('AWS_SECRET_ACCESS_KEY', ''),
                    "AWS_DEFAULT_REGION": os.getenv('AWS_DEFAULT_REGION', 'us-west-2'),
                    "PYTHONPATH": str(project_root)
                }
            },
            "portfolio-intelligence": {
                "command": "python",
                "args": [str(project_root / "start_agents.py"), "portfolio-intelligence"],
                "description": "Redaptive Portfolio Intelligence Agent - Fortune 500 energy portfolio analysis",
                "env": {
                    "POSTGRES_HOST": os.getenv('POSTGRES_HOST', 'localhost'),
                    "POSTGRES_PORT": os.getenv('POSTGRES_PORT', '5432'),
                    "POSTGRES_DATABASE": os.getenv('POSTGRES_DATABASE', 'energy_db'),
                    "DB_USER_ENERGY": os.getenv('DB_USER_ENERGY', 'energy_user'),
                    "DB_USERPASSWORD_ENERGY": os.getenv('DB_USERPASSWORD_ENERGY', 'energy123'),
                    "PYTHONPATH": str(project_root)
                }
            },
            "energy-monitoring": {
                "command": "python",
                "args": [str(project_root / "start_agents.py"), "energy-monitoring"],
                "description": "Redaptive Real-time Energy Monitoring Agent - 12k+ meter IoT processing",
                "env": {
                    "PYTHONPATH": str(project_root)
                }
            },
            "energy-finance": {
                "command": "python",
                "args": [str(project_root / "start_agents.py"), "energy-finance"],
                "description": "Redaptive Energy Project Finance Agent - EaaS revenue optimization",
                "env": {
                    "PYTHONPATH": str(project_root)
                }
            },
            "document-processing": {
                "command": "python",
                "args": [str(project_root / "start_agents.py"), "document-processing"],
                "description": "Redaptive Document Processing Agent - Utility bills, ESG reports, certificates",
                "env": {
                    "AWS_ACCESS_KEY_ID": os.getenv('AWS_ACCESS_KEY_ID', ''),
                    "AWS_SECRET_ACCESS_KEY": os.getenv('AWS_SECRET_ACCESS_KEY', ''),
                    "AWS_DEFAULT_REGION": os.getenv('AWS_DEFAULT_REGION', 'us-west-2'),
                    "PYTHONPATH": str(project_root)
                }
            },
            "summarize": {
                "command": "python",
                "args": [str(project_root / "start_agents.py"), "summarize"],
                "description": "Redaptive AI Summarization Agent - Google Gemini powered text analysis",
                "env": {
                    "GOOGLE_API_KEY": os.getenv('GOOGLE_API_KEY', ''),
                    "PYTHONPATH": str(project_root)
                }
            },
            "time": {
                "command": "uvx",
                "args": ["mcp-server-time"],
                "description": "Official MCP Time Server - Time and timezone utilities"
            }
        }
    }
    
    # Write the configuration to the file
    with open(config_path, 'w') as f:
        json.dump(mcp_config, f, indent=2)
    
    return config_path, mcp_config

def validate_environment():
    """Validate environment variables and provide recommendations"""
    
    print("🔍 Validating environment configuration...")
    
    required_vars = {
        'POSTGRES_HOST': 'Database host (default: localhost)',
        'POSTGRES_DATABASE': 'Database name (default: energy_db)',
        'DB_USER_ENERGY': 'Database user (default: energy_user)',
        'DB_USERPASSWORD_ENERGY': 'Database password'
    }
    
    optional_vars = {
        'GOOGLE_API_KEY': 'Required for AI summarization features',
        'AWS_ACCESS_KEY_ID': 'Required for document processing features',
        'AWS_SECRET_ACCESS_KEY': 'Required for document processing features'
    }
    
    missing_required = []
    missing_optional = []
    
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_required.append(f"  {var}: {description}")
    
    for var, description in optional_vars.items():
        if not os.getenv(var):
            missing_optional.append(f"  {var}: {description}")
    
    if missing_required:
        print("❌ Missing required environment variables:")
        for var in missing_required:
            print(var)
        print("\nPlease set these in your .env file.")
    else:
        print("✅ All required environment variables are set")
    
    if missing_optional:
        print("\n⚠️ Missing optional environment variables:")
        for var in missing_optional:
            print(var)
        print("\nThese are optional but enable additional features.")
    
    return len(missing_required) == 0

def show_usage_instructions(config_path):
    """Show instructions for using the generated configuration"""
    
    print(f"\n🎯 Cursor IDE MCP Configuration Generated")
    print(f"📁 Configuration saved to: {config_path}")
    print(f"📁 File size: {os.path.getsize(config_path)} bytes")
    
    print("\n🚀 Next Steps:")
    print("1. Restart Cursor IDE to load the new MCP configuration")
    print("2. Open a new chat and try these commands:")
    print("   • 'Analyze energy portfolio P001'")
    print("   • 'Calculate ROI for LED retrofit project'")
    print("   • 'Process utility bill document'")
    print("   • 'Monitor energy meters for anomalies'")
    
    print("\n🔧 Available MCP Servers:")
    print("   • redaptive-orchestrator: Natural language energy management")
    print("   • portfolio-intelligence: Fortune 500 portfolio analysis")
    print("   • energy-monitoring: Real-time IoT meter processing")
    print("   • energy-finance: EaaS revenue optimization")
    print("   • document-processing: Utility bills and ESG reports")
    print("   • summarize: AI-powered text analysis")
    print("   • time: Official time and timezone utilities")
    
    print(f"\n📚 For troubleshooting, see: README.md")

def main():
    """Main function to generate Cursor MCP configuration"""
    
    print("🔌 Cursor IDE MCP Configuration Generator")
    print("=" * 50)
    
    # Validate environment
    env_valid = validate_environment()
    
    if not env_valid:
        print("\n❌ Environment validation failed. Please fix the issues above.")
        print("💡 Tip: Copy .env.example to .env and update the values")
        return 1
    
    try:
        # Generate configuration
        config_path, config = generate_cursor_mcp_config()
        
        print(f"\n✅ Successfully generated Cursor MCP configuration")
        print(f"📊 Generated {len(config['mcpServers'])} MCP server configurations")
        
        # Show usage instructions
        show_usage_instructions(config_path)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error generating configuration: {e}")
        return 1

if __name__ == "__main__":
    exit(main())