#!/usr/bin/env python3
"""Test script to demonstrate learning-based execution planning."""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners import DynamicPlanner, LearningBasedPlanner, HybridPlanner

async def test_learning_based_planning():
    """Test learning-based planning vs rule-based planning."""
    
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
    
    print("🤖 **Learning-Based vs Rule-Based Planning Comparison**\n")
    
    # Initialize planners
    rule_based_planner = DynamicPlanner()
    learning_based_planner = LearningBasedPlanner()
    
    available_agents = ["energy-monitoring", "energy-finance", "portfolio-intelligence", "system"]
    
    for query in test_queries:
        print(f"📝 **Query**: {query}")
        print("-" * 60)
        
        # Test rule-based planner
        print("🔧 **Rule-Based Planning**:")
        try:
            rule_result = await rule_based_planner.create_workflow(query, available_agents)
            print(f"  Workflow ID: {rule_result.get('workflow_id', 'N/A')}")
            print(f"  Planning Method: {rule_result.get('planning_method', 'N/A')}")
            print(f"  Steps: {len(rule_result.get('steps', []))}")
            if rule_result.get('steps'):
                step = rule_result['steps'][0]
                print(f"  Agent: {step.get('agent', 'N/A')}")
                print(f"  Tool: {step.get('tool', 'N/A')}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Test learning-based planner
        print("\n🧠 **Learning-Based Planning**:")
        try:
            learning_result = await learning_based_planner.create_workflow(query, available_agents)
            print(f"  Workflow ID: {learning_result.get('workflow_id', 'N/A')}")
            print(f"  Planning Method: {learning_result.get('planning_method', 'N/A')}")
            print(f"  Planning Reason: {learning_result.get('planning_reason', 'N/A')}")
            print(f"  Steps: {len(learning_result.get('steps', []))}")
            if learning_result.get('steps'):
                step = learning_result['steps'][0]
                print(f"  Agent: {step.get('agent', 'N/A')}")
                print(f"  Tool: {step.get('tool', 'N/A')}")
                print(f"  Reasoning: {step.get('reasoning', 'N/A')}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print("\n" + "=" * 80 + "\n")

async def test_hybrid_planning():
    """Test hybrid planning approach."""
    
    print("🎯 **Hybrid Planning Strategy**\n")
    
    # Test queries
    test_queries = [
        "What is the date of the most recent energy usage reading?",
        "Calculate ROI for LED retrofit project",
        "Find energy optimization opportunities",
        "Who was the first president of the United States?"
    ]
    
    # Test different planner configurations
    planners = {
        "Rule-Based Only": DynamicPlanner(),
        "Learning-Based Only": LearningBasedPlanner(),
        "Hybrid (Learning Primary)": HybridPlanner(learning_primary=True),
        "Hybrid (Rule Primary)": HybridPlanner(learning_primary=False)
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
                print(f"   Method: {result.get('planning_method', 'N/A')}")
                print(f"   Steps: {len(result.get('steps', []))}")
                if result.get('steps'):
                    step = result['steps'][0]
                    print(f"   Agent: {step.get('agent', 'N/A')}")
                    print(f"   Tool: {step.get('tool', 'N/A')}")
                print()
            except Exception as e:
                print(f"❌ Error with {query}: {e}")
        
        print("-" * 60 + "\n")

async def test_llm_client():
    """Test the LLM client directly."""
    
    print("🧠 **LLM Client Test**\n")
    
    try:
        from redaptive.orchestration.planners.llm_client import LLMClient
        
        # Test with different providers
        providers = ["anthropic", "openai"]
        
        for provider in providers:
            print(f"🔧 Testing {provider.upper()} provider:")
            try:
                client = LLMClient(provider=provider)
                print(f"  ✅ {provider.upper()} client initialized")
                
                # Test a simple generation
                test_prompt = "Respond with just 'Test successful' if you can see this message."
                response = await client.generate(test_prompt)
                print(f"  📝 Response: {response[:100]}...")
                
            except Exception as e:
                print(f"  ❌ {provider.upper()} client error: {e}")
            
            print()
            
    except ImportError as e:
        print(f"❌ Could not import LLMClient: {e}")

def main():
    """Run all learning-based planning tests."""
    print("🚀 Learning-Based Execution Planning Tests")
    print("=" * 60)
    
    # Check environment
    print("🔍 Environment Check:")
    print(f"  PREFERRED_LLM_PROVIDER: {os.getenv('PREFERRED_LLM_PROVIDER', 'Not set')}")
    print(f"  ANTHROPIC_API_KEY: {'Set' if os.getenv('ANTHROPIC_API_KEY') else 'Not set'}")
    print(f"  OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    print()
    
    # Run tests
    asyncio.run(test_learning_based_planning())
    asyncio.run(test_hybrid_planning())
    asyncio.run(test_llm_client())
    
    print("✅ Learning-based execution planning tests completed!")

if __name__ == "__main__":
    main() 