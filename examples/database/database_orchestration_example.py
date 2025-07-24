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
sys.path.insert(0, str(project_root / "src"))

from redaptive.orchestration import OrchestrationEngine
from redaptive.agents import AGENT_REGISTRY

async def process_user_request(user_request: str, **context):
    """
    Process a user request using the orchestration engine.
    This is a simplified version that demonstrates the concept.
    """
    try:
        # Initialize the orchestration engine
        engine = OrchestrationEngine()
        
        # Initialize database agents (using energy agents for demo)
        agent_names = ["portfolio-intelligence", "energy-monitoring"]
        success = await engine.initialize_agents(agent_names)
        
        if not success:
            return {
                "error": "Failed to initialize agents",
                "workflow": "database_operations",
                "user_goal": user_request,
                "steps_executed": 0
            }
        
        # For demo purposes, return a mock result
        # In a real implementation, this would analyze the request and execute workflows
        return {
            "workflow": "database_operations",
            "user_goal": user_request,
            "steps_executed": 2,
            "summary": f"Processed database request: {user_request}",
            "results": {
                "step_1": {
                    "agent": "portfolio-intelligence",
                    "tool": "search_facilities",
                    "result": {
                        "content": [{"text": "Found 5 buildings in Zurich with energy data"}],
                        "isError": False
                    }
                },
                "step_2": {
                    "agent": "energy-monitoring",
                    "tool": "analyze_usage_patterns",
                    "result": {
                        "content": [{"text": "Analyzed consumption patterns for last 6 months"}],
                        "isError": False
                    }
                }
            }
        }
        
    except Exception as e:
        return {
            "error": f"Failed to process request: {str(e)}",
            "workflow": "database_operations",
            "user_goal": user_request,
            "steps_executed": 0
        }

async def main():
    """Run database operations orchestration example"""
    
    # Initialize the orchestrator
    engine = OrchestrationEngine()
    
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