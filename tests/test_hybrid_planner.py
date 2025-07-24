#!/usr/bin/env python3
"""Test script to demonstrate hybrid planner approach."""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners import HybridPlanner, DynamicPlanner, LLMPlanner
from redaptive.config.planner_config import PlannerConfig

async def test_hybrid_approach():
    """Test the hybrid planner approach."""
    
    print("🎯 **Hybrid Planner Strategy**\n")
    
    # Test queries
    test_queries = [
        "What is the date of the most recent energy usage reading?",
        "Calculate ROI for LED retrofit project",
        "Find energy optimization opportunities",
        "Who was the first president of the United States?"
    ]
    
    # Test different planner configurations
    planners = {
        "Hardcoded Only": DynamicPlanner(),
        "LLM Only": LLMPlanner(),
        "Hybrid (LLM Primary)": HybridPlanner(llm_primary=True),
        "Hybrid (Hardcoded Primary)": HybridPlanner(llm_primary=False)
    }
    
    available_agents = ["energy-monitoring", "energy-finance", "portfolio-intelligence", "system"]
    
    for planner_name, planner in planners.items():
        print(f"🔧 **{planner_name}**")
        print("=" * 60)
        
        for query in test_queries:
            try:
                result = await planner.create_workflow(query, available_agents)
                print(f"📝 Query: {query}")
                print(f"   Workflow: {result.get('workflow_id', 'N/A')}")
                print(f"   Steps: {len(result.get('steps', []))}")
                if result.get('steps'):
                    step = result['steps'][0]
                    print(f"   Agent: {step.get('agent', 'N/A')}")
                    print(f"   Tool: {step.get('tool', 'N/A')}")
                print()
            except Exception as e:
                print(f"❌ Error with {query}: {e}")
        
        print("-" * 60 + "\n")

async def test_planner_config():
    """Test the planner configuration system."""
    
    print("⚙️ **Planner Configuration System**\n")
    
    configs = [
        ("hardcoded", "Hardcoded Planner"),
        ("llm", "LLM Planner"), 
        ("hybrid", "Hybrid Planner")
    ]
    
    for config_type, name in configs:
        config = PlannerConfig(config_type)
        planner_class = config.get_planner_class()
        planner_kwargs = config.get_planner_kwargs()
        
        print(f"🔧 **{name}**")
        print(f"   Type: {config.planner_type.value}")
        print(f"   Class: {planner_class.__name__}")
        print(f"   Args: {planner_kwargs}")
        print()

if __name__ == "__main__":
    print("🚀 Testing Hybrid Planner Strategy\n")
    asyncio.run(test_hybrid_approach())
    asyncio.run(test_planner_config()) 