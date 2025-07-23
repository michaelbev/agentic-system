#!/usr/bin/env python3
"""
Database Operations Orchestration Example
Demonstrates intelligent orchestration for database operations
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from orchestration.intelligent.intelligent_orchestrator import IntelligentOrchestrator, process_user_request

async def main():
    """Run database operations orchestration example"""
    
    # Initialize the orchestrator
    orchestrator = IntelligentOrchestrator()
    
    print("🚀 Database Operations Orchestration Example")
    print("=" * 50)
    
    # Example 1: Query energy data
    print("\n⚡ Example 1: Query energy data")
    print("-" * 40)
    
    request = "Show me all buildings in Zurich with their energy consumption and efficiency ratings"
    
    try:
        result = await process_user_request(request)
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Analyze energy consumption patterns
    print("\n📊 Example 2: Analyze energy consumption patterns")
    print("-" * 40)
    
    request = "Analyze energy consumption patterns for the last 6 months and show efficiency trends"
    
    try:
        result = await process_user_request(request)
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Database maintenance
    print("\n🔧 Example 3: Database maintenance")
    print("-" * 40)
    
    request = "Check database health and optimize performance"
    
    try:
        result = await process_user_request(request)
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 4: Data migration
    print("\n🔄 Example 4: Data migration")
    print("-" * 40)
    
    request = "Migrate old energy data to the new schema format"
    
    try:
        result = await process_user_request(request)
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 