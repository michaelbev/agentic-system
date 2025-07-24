#!/usr/bin/env python3
"""Test script to demonstrate LLM-based vs hardcoded planning."""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners import DynamicPlanner, LLMPlanner

async def test_planning_comparison():
    """Compare hardcoded vs LLM-based planning."""
    
    # Test queries with variations
    test_queries = [
        "What is the date of the most recent energy usage reading?",
        "Get the latest meter readings",
        "Show me the most recent energy data",
        "What's the current time?",
        "Calculate ROI for LED retrofit project",
        "Find energy optimization opportunities",
        "Who was the first president of the United States?"
    ]
    
    print("🤖 **Planning Method Comparison**\n")
    
    # Initialize planners
    hardcoded_planner = DynamicPlanner()
    llm_planner = LLMPlanner()
    
    available_agents = ["energy-monitoring", "energy-finance", "portfolio-intelligence", "system"]
    
    for query in test_queries:
        print(f"📝 **Query**: {query}")
        print("-" * 60)
        
        # Test hardcoded planner
        print("🔧 **Hardcoded Planning**:")
        try:
            hardcoded_result = await hardcoded_planner.create_workflow(query, available_agents)
            print(f"  Workflow ID: {hardcoded_result.get('workflow_id', 'N/A')}")
            print(f"  Steps: {len(hardcoded_result.get('steps', []))}")
            if hardcoded_result.get('steps'):
                step = hardcoded_result['steps'][0]
                print(f"  Agent: {step.get('agent', 'N/A')}")
                print(f"  Tool: {step.get('tool', 'N/A')}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Test LLM planner
        print("\n🧠 **LLM-Based Planning**:")
        try:
            llm_result = await llm_planner.create_workflow(query, available_agents)
            print(f"  Workflow ID: {llm_result.get('workflow_id', 'N/A')}")
            print(f"  Reasoning: {llm_result.get('reasoning', 'N/A')}")
            print(f"  Steps: {len(llm_result.get('steps', []))}")
            if llm_result.get('steps'):
                step = llm_result['steps'][0]
                print(f"  Agent: {step.get('agent', 'N/A')}")
                print(f"  Tool: {step.get('tool', 'N/A')}")
                print(f"  Reasoning: {step.get('reasoning', 'N/A')}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    asyncio.run(test_planning_comparison()) 