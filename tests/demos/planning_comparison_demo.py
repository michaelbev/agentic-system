#!/usr/bin/env python3
"""Demo script to compare different planning methods."""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent.parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners import DynamicPlanner, LearningBasedPlanner, HybridPlanner

async def planning_comparison_demo():
    """Demonstrate different planning methods in action."""
    
    print("🚀 Planning Methods Comparison Demo")
    print("=" * 60)
    
    # Environment check
    print("🔍 Environment Configuration:")
    print(f"  PREFERRED_LLM_PROVIDER: {os.getenv('PREFERRED_LLM_PROVIDER', 'Not set')}")
    print(f"  ANTHROPIC_API_KEY: {'✅ Set' if os.getenv('ANTHROPIC_API_KEY') else '❌ Not set'}")
    print()
    
    # Initialize planners
    planners = {
        "Rule-Based": DynamicPlanner(),
        "Learning-Based": LearningBasedPlanner(),
        "Hybrid (Learning Primary)": HybridPlanner(learning_primary=True),
        "Hybrid (Rule Primary)": HybridPlanner(learning_primary=False)
    }
    
    available_agents = ["energy-monitoring", "energy-finance", "portfolio-intelligence", "system"]
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Energy Data Query",
            "query": "What is the date of the most recent energy usage reading?",
            "expected_agent": "energy-monitoring",
            "expected_tool": "get_latest_energy_reading"
        },
        {
            "name": "Financial Analysis",
            "query": "Calculate ROI for LED retrofit project",
            "expected_agent": "energy-finance",
            "expected_tool": "calculate_project_roi"
        },
        {
            "name": "Portfolio Optimization",
            "query": "Find energy optimization opportunities",
            "expected_agent": "portfolio-intelligence",
            "expected_tool": "identify_optimization_opportunities"
        },
        {
            "name": "System Time Query",
            "query": "What's the current time?",
            "expected_agent": "system",
            "expected_tool": "get_current_time"
        }
    ]
    
    print("🤖 **Planning Method Comparison**\n")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"📝 **Test {i}**: {scenario['name']}")
        print(f"   Query: {scenario['query']}")
        print("-" * 50)
        
        for planner_name, planner in planners.items():
            try:
                result = await planner.create_workflow(scenario['query'], available_agents)
                
                # Determine status
                if result.get('steps'):
                    step = result['steps'][0]
                    agent_match = step.get('agent') == scenario['expected_agent']
                    tool_match = step.get('tool') == scenario['expected_tool']
                    
                    if agent_match and tool_match:
                        status = "✅ PASS"
                    else:
                        status = "⚠️  PARTIAL"
                else:
                    status = "❌ FAIL"
                
                print(f"  {planner_name:25} : {status}")
                print(f"    Workflow: {result.get('workflow_id', 'N/A')}")
                print(f"    Method: {result.get('planning_method', 'N/A')}")
                if result.get('steps'):
                    step = result['steps'][0]
                    print(f"    Agent: {step.get('agent', 'N/A')}")
                    print(f"    Tool: {step.get('tool', 'N/A')}")
                
            except Exception as e:
                print(f"  {planner_name:25} : ❌ ERROR - {e}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("✅ Planning comparison demo completed!")
    print("\n🎯 **Key Insights**:")
    print("  • Rule-based planning provides consistent, predictable results")
    print("  • Learning-based planning uses AI to understand natural language")
    print("  • Hybrid planning combines both approaches for reliability")
    print("  • All methods can route queries to appropriate agents")

if __name__ == "__main__":
    asyncio.run(planning_comparison_demo()) 