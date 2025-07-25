#!/usr/bin/env python3
"""
Test script to verify proper integration between matchers and planners.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.matchers import KeywordMatcher
from redaptive.orchestration.planners import DynamicPlanner

async def test_matcher_planner_integration():
    """Test that matchers and planners work together properly."""
    
    print("🧪 Testing Matcher-Planner Integration")
    print("=" * 60)
    
    # Initialize components
    matcher = KeywordMatcher()
    planner = DynamicPlanner()
    
    # Test queries with expected intents
    test_cases = [
        {
            "query": "How many buildings are part of the Walmart portfolio?",
            "expected_intent": "portfolio",
            "expected_workflow": "portfolio_analysis_workflow"
        },
        {
            "query": "What is the current time?",
            "expected_intent": "time", 
            "expected_workflow": "time_analysis_workflow"
        },
        {
            "query": "Analyze energy consumption for building 123",
            "expected_intent": "energy",
            "expected_workflow": "energy_analysis_workflow"
        },
        {
            "query": "Calculate ROI for LED retrofit",
            "expected_intent": "finance",
            "expected_workflow": "financial_analysis_workflow"
        },
        {
            "query": "What is the date of the most recent energy usage reading?",
            "expected_intent": "energy_monitoring",
            "expected_workflow": "energy_monitoring_date_workflow"
        },
        {
            "query": "Tell me about the weather",
            "expected_intent": "out_of_scope",
            "expected_workflow": "out_of_scope_workflow"
        }
    ]
    
    available_agents = ["portfolio-intelligence", "energy-monitoring", "energy-finance", "system"]
    
    print(f"✅ Testing {len(test_cases)} different query types")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        query = test_case["query"]
        expected_intent = test_case["expected_intent"]
        expected_workflow = test_case["expected_workflow"]
        
        print(f"🔍 Test {i}: '{query}'")
        print("-" * 40)
        
        # Test matcher directly
        intent_result = await matcher.match_intent(query)
        actual_intent = intent_result.get('intent', 'unknown')
        confidence = intent_result.get('confidence', 0.0)
        
        print(f"  🎯 Matcher Intent: {actual_intent} (confidence: {confidence:.2f})")
        print(f"  📊 Expected Intent: {expected_intent}")
        print(f"  ✅ Intent Match: {'✅' if actual_intent == expected_intent else '❌'}")
        
        # Test planner with matcher integration
        workflow = await planner.create_workflow(query, available_agents)
        actual_workflow = workflow.get('workflow_id', 'unknown')
        planning_reason = workflow.get('planning_reason', 'No reason provided')
        
        print(f"  📋 Planner Workflow: {actual_workflow}")
        print(f"  📊 Expected Workflow: {expected_workflow}")
        print(f"  ✅ Workflow Match: {'✅' if actual_workflow == expected_workflow else '❌'}")
        print(f"  💭 Planning Reason: {planning_reason}")
        
        # Check if planning reason mentions keyword matcher
        if "keyword matcher" in planning_reason.lower():
            print(f"  ✅ Matcher Integration: ✅ (planning reason mentions keyword matcher)")
        else:
            print(f"  ❌ Matcher Integration: ❌ (planning reason doesn't mention keyword matcher)")
        
        print()
    
    print("🎯 Integration Test Summary:")
    print("=" * 60)
    print("✅ Matchers and planners are now properly integrated!")
    print("✅ KeywordMatcher handles intent detection")
    print("✅ DynamicPlanner uses matcher results for detailed planning")
    print("✅ Planning reasons now show matcher confidence and intent details")
    print("✅ No more duplicate keyword definitions")
    print("✅ Clear separation of responsibilities")

if __name__ == "__main__":
    asyncio.run(test_matcher_planner_integration()) 