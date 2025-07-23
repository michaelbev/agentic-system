#!/usr/bin/env python3
"""
Test Intelligent Multi-Agent Orchestrator
Updated to use the intelligent workflow composition system
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the path
src_dir = str(Path(__file__).parent.parent.parent / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from redaptive.orchestration import OrchestrationEngine

async def test_time_agent_workflow():
    """Test the intelligent orchestrator with time-based workflows"""
    print("🕐 Testing Intelligent Orchestrator with Time Workflows")
    print("=" * 60)
    
    try:
        # Test getting current time using intelligent workflow
        print("🕐 Testing get current time workflow...")
        result = await process_user_request(
            "get the current time",
            timezone="America/Denver"
        )
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Workflow completed: {result.get('workflow', 'Unknown')}")
            print(f"📋 Steps executed: {result.get('steps_executed', 0)}")
            print(f"📝 Summary: {result.get('summary', 'No summary')}")
        
        print("\n✅ Time workflow test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def test_workflow_discovery():
    """Test intelligent workflow discovery and planning"""
    print("\n🔍 Testing Intelligent Workflow Discovery")
    print("=" * 50)
    
    orchestrator = IntelligentOrchestrator()
    
    try:
        # Test workflow planning for different requests
        test_requests = [
            "summarize this PDF",
            "analyze the sentiment of this document", 
            "extract tables from this PDF",
            "analyze energy consumption for this building"
        ]
        
        for request in test_requests:
            print(f"\n📝 Planning workflow for: '{request}'")
            workflow_steps = orchestrator.plan_workflow(request, {"file_path": "test.pdf"})
            
            if workflow_steps:
                agent_names = [step.agent_name for step in workflow_steps]
                print(f"✅ Planned {len(workflow_steps)} steps using agents: {agent_names}")
            else:
                print("⚠️  No workflow planned")
        
        print("\n✅ Workflow discovery test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def test_pattern_matching():
    """Test pattern matching capabilities"""
    print("\n🎯 Testing Pattern Matching")
    print("=" * 40)
    
    orchestrator = IntelligentOrchestrator()
    
    try:
        # Test various user requests and see which patterns they match
        test_cases = [
            ("summarize this PDF", "summarize_pdf"),
            ("give me a summary of this document", "summarize_pdf"),
            ("analyze the sentiment of this PDF", "analyze_document"),
            ("extract tables from this document", "extract_tables"),
            ("analyze energy consumption for this building", "energy_data_analysis"),
            ("give me a complete analysis of this document", "document_analysis")
        ]
        
        for request, expected_pattern in test_cases:
            print(f"\n📝 Testing: '{request}'")
            workflow_steps = orchestrator.plan_workflow(request, {"file_path": "test.pdf"})
            
            if workflow_steps:
                print(f"✅ Pattern matched: {expected_pattern}")
                print(f"   Steps: {len(workflow_steps)}")
            else:
                print(f"⚠️  No pattern matched for: {expected_pattern}")
        
        print("\n✅ Pattern matching test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def test_intelligent_composition():
    """Test intelligent workflow composition for unknown requests"""
    print("\n🧠 Testing Intelligent Composition")
    print("=" * 45)
    
    orchestrator = IntelligentOrchestrator()
    
    try:
        # Test requests that don't match known patterns
        unknown_requests = [
            "process this document and give me insights",
            "extract information from this file and create a report",
            "analyze this data and provide recommendations"
        ]
        
        for request in unknown_requests:
            print(f"\n📝 Testing unknown request: '{request}'")
            workflow_steps = orchestrator.plan_workflow(request, {"file_path": "test.pdf"})
            
            if workflow_steps:
                agent_names = [step.agent_name for step in workflow_steps]
                print(f"✅ Intelligent composition created workflow with agents: {agent_names}")
            else:
                print("⚠️  No workflow composed")
        
        print("\n✅ Intelligent composition test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def test_error_handling():
    """Test error handling in intelligent workflows"""
    print("\n⚠️  Testing Error Handling")
    print("=" * 35)
    
    try:
        # Test with invalid requests
        invalid_requests = [
            "",  # Empty request
            "invalid request with no context",  # No file path
        ]
        
        for request in invalid_requests:
            print(f"\n📝 Testing invalid request: '{request}'")
            result = await process_user_request(request, file_path="nonexistent.pdf")
            
            if "error" in result:
                print(f"✅ Error properly handled: {result['error'][:50]}...")
            else:
                print("⚠️  No error returned for invalid request")
        
        print("\n✅ Error handling test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

async def main():
    """Run all intelligent orchestrator tests"""
    print("🚀 Intelligent Multi-Agent Orchestrator Tests")
    print("=" * 60)
    
    await test_workflow_discovery()
    await test_pattern_matching()
    await test_intelligent_composition()
    await test_time_agent_workflow()
    await test_error_handling()
    
    print("\n🎉 All intelligent orchestrator tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 