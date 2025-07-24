#!/usr/bin/env python3
"""
Test script to verify energy-specific date queries are routed correctly
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from redaptive.orchestration.engine import OrchestrationEngine
from redaptive.orchestration.matchers.keyword_matcher import KeywordMatcher
from redaptive.orchestration.planners.dynamic_planner import DynamicPlanner

async def test_energy_date_query():
    """Test that energy-specific date queries are routed to energy monitoring agent"""
    
    print("🧪 Testing Energy-Specific Date Query Routing")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "what is the date of the most recent energy usage reading?",
        "when was the last energy consumption reading?",
        "what is the latest meter reading date?",
        "show me the most recent energy data timestamp",
        "when did we last get energy usage data?"
    ]
    
    # Initialize components
    matcher = KeywordMatcher()
    planner = DynamicPlanner()
    engine = OrchestrationEngine()
    
    # Initialize agents
    await engine.initialize_agents([
        "portfolio-intelligence",
        "energy-monitoring", 
        "energy-finance",
        "document-processing",
        "summarize",
        "system"
    ])
    
    print(f"✅ Initialized {len(engine.agents)} agents")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: '{query}'")
        print("-" * 40)
        
        # Test intent matching
        intent_result = await matcher.match_intent(query)
        print(f"🎯 Intent: {intent_result['intent']} (confidence: {intent_result['confidence']:.2f})")
        print(f"📝 Reason: {intent_result.get('reason', 'N/A')}")
        
        # Test workflow planning
        workflow = await planner.create_workflow(query, list(engine.agents.keys()))
        print(f"📋 Workflow: {workflow['workflow_id']}")
        
        # Show workflow steps
        for j, step in enumerate(workflow['steps'], 1):
            print(f"  Step {j}: {step['agent']} -> {step['tool']}")
        
        # Test execution
        try:
            result = await engine.execute_workflow(f"test_workflow_{i}", workflow)
            print(f"✅ Execution successful")
            
            # Check if energy monitoring agent was used
            energy_monitoring_used = any(
                step.get('agent') == 'energy-monitoring' 
                for step in workflow['steps']
            )
            
            if energy_monitoring_used:
                print(f"🎯 CORRECT: Energy monitoring agent was used for energy date query")
            else:
                print(f"❌ INCORRECT: Energy monitoring agent was NOT used for energy date query")
                
        except Exception as e:
            print(f"❌ Execution failed: {e}")
        
        print()

async def main():
    """Main test function"""
    await test_energy_date_query()

if __name__ == "__main__":
    asyncio.run(main()) 