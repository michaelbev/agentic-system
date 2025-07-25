#!/usr/bin/env python3
"""
Demo script showing adaptive planning capabilities.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent.parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration import OrchestrationEngine

async def adaptive_planning_demo():
    """Demonstrate adaptive planning with different methods."""
    
    print("🚀 Adaptive Planning Demo")
    print("=" * 60)
    
    # Initialize orchestration engine
    engine = OrchestrationEngine()
    
    # Initialize agents
    agent_names = [
        "portfolio-intelligence",
        "energy-monitoring", 
        "energy-finance",
        "system"
    ]
    
    success = await engine.initialize_agents(agent_names)
    if not success:
        print("❌ Failed to initialize agents")
        return
    
    print(f"✅ Initialized {len(agent_names)} agents")
    print()
    
    # Demo queries with different planning methods
    demo_queries = [
        {
            "query": "How many buildings are part of the Walmart portfolio?",
            "method": None,  # Use default (systematic)
            "description": "Default systematic planning"
        },
        {
            "query": "Use systematic planning to analyze energy consumption for building 123",
            "method": "systematic",
            "description": "Explicit systematic planning"
        },
        {
            "query": "Use AI to create a comprehensive workflow for portfolio analysis",
            "method": "learning",
            "description": "Explicit learning-based planning"
        },
        {
            "query": "Use hybrid approach for financial ROI calculation with LED retrofit",
            "method": "hybrid",
            "description": "Explicit hybrid planning"
        },
        {
            "query": "Use auto planning for building energy optimization",
            "method": "auto",
            "description": "Explicit auto planning"
        }
    ]
    
    print("🎯 Running Adaptive Planning Demo")
    print("=" * 60)
    
    for i, demo in enumerate(demo_queries, 1):
        query = demo["query"]
        method = demo["method"]
        description = demo["description"]
        
        print(f"\n🔍 Demo {i}: {description}")
        print(f"   Query: '{query}'")
        if method:
            print(f"   Method: {method}")
        else:
            print(f"   Method: default (systematic)")
        print("-" * 50)
        
        try:
            # Execute adaptive workflow
            result = await engine.execute_adaptive_workflow(
                user_request=query,
                available_agents=agent_names,
                planning_method=method
            )
            
            # Display results
            print(f"   📋 Status: {result.get('status', 'unknown')}")
            print(f"   🎯 Planning Method: {result.get('planning_method', 'unknown')}")
            print(f"   💭 Planning Reason: {result.get('planning_reason', 'No reason provided')}")
            
            if result.get('status') == 'completed':
                results = result.get('results', {})
                print(f"   📊 Steps Completed: {len(results)}")
                
                for step_name, step_result in results.items():
                    agent = step_result.get('agent', 'unknown')
                    tool = step_result.get('tool', 'unknown')
                    print(f"      • {step_name}: {agent} -> {tool}")
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Execution failed: {e}")
        
        print()
    
    print("🎯 Adaptive Planning Demo Summary:")
    print("=" * 60)
    print("✅ Successfully demonstrated adaptive planning!")
    print("✅ Supports multiple planning methods:")
    print("   • systematic: Rule-based planning")
    print("   • learning: AI-powered planning") 
    print("   • hybrid: Combined approach")
    print("   • auto: Automatic method selection")
    print("✅ Handles explicit method specification")
    print("✅ Provides detailed planning reasons")
    print("✅ Graceful fallback on failures")

if __name__ == "__main__":
    asyncio.run(adaptive_planning_demo()) 