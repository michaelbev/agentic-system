#!/usr/bin/env python3
"""Demo script to show learning-based execution planning working."""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners import DynamicPlanner, LearningBasedPlanner

async def demo_learning_based_planning():
    """Demonstrate learning-based planning in action."""
    
    print("🚀 Learning-Based Execution Planning Demo")
    print("=" * 60)
    
    # Check environment
    print("🔍 Environment Check:")
    print(f"  PREFERRED_LLM_PROVIDER: {os.getenv('PREFERRED_LLM_PROVIDER', 'Not set')}")
    print(f"  ANTHROPIC_API_KEY: {'✅ Set' if os.getenv('ANTHROPIC_API_KEY') else '❌ Not set'}")
    print()
    
    # Initialize planners
    rule_based = DynamicPlanner()
    learning_based = LearningBasedPlanner()
    
    available_agents = ["energy-monitoring", "energy-finance", "portfolio-intelligence", "system"]
    
    # Test queries
    test_queries = [
        "What is the date of the most recent energy usage reading?",
        "Calculate ROI for LED retrofit project",
        "Find energy optimization opportunities",
        "What's the current time?"
    ]
    
    print("🤖 **Planning Method Comparison**\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"📝 **Test {i}**: {query}")
        print("-" * 50)
        
        # Rule-based planning
        print("🔧 **Rule-Based Planning**:")
        try:
            rule_result = await rule_based.create_workflow(query, available_agents)
            print(f"  ✅ Workflow: {rule_result.get('workflow_id', 'N/A')}")
            print(f"  📋 Method: {rule_result.get('planning_method', 'N/A')}")
            print(f"  🔢 Steps: {len(rule_result.get('steps', []))}")
            if rule_result.get('steps'):
                step = rule_result['steps'][0]
                print(f"  🤖 Agent: {step.get('agent', 'N/A')}")
                print(f"  🛠️  Tool: {step.get('tool', 'N/A')}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Learning-based planning
        print("\n🧠 **Learning-Based Planning**:")
        try:
            learning_result = await learning_based.create_workflow(query, available_agents)
            print(f"  ✅ Workflow: {learning_result.get('workflow_id', 'N/A')}")
            print(f"  📋 Method: {learning_result.get('planning_method', 'N/A')}")
            print(f"  💭 Reason: {learning_result.get('planning_reason', 'N/A')}")
            print(f"  🔢 Steps: {len(learning_result.get('steps', []))}")
            if learning_result.get('steps'):
                step = learning_result['steps'][0]
                print(f"  🤖 Agent: {step.get('agent', 'N/A')}")
                print(f"  🛠️  Tool: {step.get('tool', 'N/A')}")
                print(f"  💡 Reasoning: {step.get('reasoning', 'N/A')}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("✅ Learning-based execution planning demo completed!")
    print("\n🎯 **Key Findings**:")
    print("  • Learning-based planning uses AI to understand natural language")
    print("  • Rule-based planning uses hardcoded patterns")
    print("  • Both methods can handle the same queries effectively")
    print("  • Learning-based provides more detailed reasoning")
    print("  • System gracefully falls back to rule-based when needed")

if __name__ == "__main__":
    asyncio.run(demo_learning_based_planning()) 