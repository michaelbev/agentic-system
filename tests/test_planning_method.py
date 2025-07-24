#!/usr/bin/env python3
"""Test script to demonstrate planning method tracking."""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners import HybridPlanner, DynamicPlanner, LLMPlanner

async def test_planning_method_tracking():
    """Test planning method tracking in results."""
    
    print("🎯 **Planning Method Tracking Test**\n")
    
    # Test queries that should trigger different planning methods
    test_queries = [
        "What is the date of the most recent energy usage reading?",
        "Calculate ROI for LED retrofit project", 
        "Find energy optimization opportunities",
        "Who was the first president of the United States?"
    ]
    
    # Test different planners
    planners = {
        "Hybrid (LLM Primary)": HybridPlanner(llm_primary=True),
        "Hybrid (Hardcoded Primary)": HybridPlanner(llm_primary=False),
        "LLM Only": LLMPlanner(),
        "Hardcoded Only": DynamicPlanner()
    }
    
    available_agents = ["energy-monitoring", "energy-finance", "portfolio-intelligence", "system"]
    
    for planner_name, planner in planners.items():
        print(f"🔧 **{planner_name}**")
        print("=" * 60)
        
        for query in test_queries:
            try:
                result = await planner.create_workflow(query, available_agents)
                
                # Extract planning method info
                method = result.get("planning_method", "unknown")
                reason = result.get("planning_reason", "No reason provided")
                
                print(f"📝 Query: {query}")
                print(f"   Workflow: {result.get('workflow_id', 'N/A')}")
                print(f"   Planning Method: {method}")
                print(f"   Planning Reason: {reason}")
                
                if result.get('steps'):
                    step = result['steps'][0]
                    print(f"   Agent: {step.get('agent', 'N/A')}")
                    print(f"   Tool: {step.get('tool', 'N/A')}")
                print()
                
            except Exception as e:
                print(f"❌ Error with {query}: {e}")
        
        print("-" * 60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_planning_method_tracking()) 