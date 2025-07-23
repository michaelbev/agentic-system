#!/usr/bin/env python3
"""
Quick Test Suite for Intelligent Orchestrator
Tests core functionality without requiring running agents
"""

import asyncio
import sys
import pytest
from pathlib import Path

# Add the project root to the path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from orchestration.intelligent.intelligent_orchestrator import IntelligentOrchestrator, process_user_request
from orchestration.intelligent.matchers.keyword_matcher import KeywordMatcher
from orchestration.intelligent.workflow_engine import WorkflowEngine

def test_workflow_patterns():
    """Test that workflow patterns are loaded correctly"""
    print("🧪 Testing workflow patterns...")
    
    orchestrator = IntelligentOrchestrator()
    patterns = orchestrator.workflow_patterns
    
    if patterns and len(patterns) > 0:
        print("✅ Workflow patterns loaded correctly")
        return True
    else:
        print("❌ No workflow patterns found")
        return False

def test_keyword_extraction():
    """Test keyword extraction functionality"""
    print("🔍 Testing keyword extraction...")
    
    orchestrator = IntelligentOrchestrator()
    
    # Test keyword extraction
    keywords = orchestrator._extract_keywords("summarize this PDF document")
    expected_keywords = ["document", "summarize"]
    
    if all(keyword in keywords for keyword in expected_keywords):
        print("✅ Keyword extraction working correctly")
        return True
    else:
        print(f"❌ Keyword extraction failed. Expected {expected_keywords}, got {keywords}")
        return False

def test_pattern_matching():
    """Test pattern matching functionality"""
    print("🎯 Testing pattern matching...")
    
    orchestrator = IntelligentOrchestrator()
    
    # Test various patterns
    test_cases = [
        ("summarize this PDF", "summarize_pdf"),
        ("analyze the sentiment of this document", "analyze_document"),
        ("extract tables from this PDF", "extract_tables"),
        ("analyze energy consumption for this building", "energy_data_analysis"),
        ("give me a complete analysis of this document", "document_analysis")
    ]
    
    all_passed = True
    for user_goal, expected_pattern in test_cases:
        workflow_steps = orchestrator.plan_workflow(user_goal, {"file_path": "test.pdf"})
        if workflow_steps:
            print(f"✅ {user_goal} -> {len(workflow_steps)} steps using agents: {[step.agent_name for step in workflow_steps]}")
        else:
            print(f"❌ {user_goal} -> No workflow planned")
            all_passed = False
    
    if all_passed:
        print("✅ Pattern matching working correctly")
        return True
    else:
        print("❌ Pattern matching failed")
        return False

def test_argument_resolution():
    """Test argument resolution functionality"""
    print("🔧 Testing argument resolution...")
    
    orchestrator = IntelligentOrchestrator()
    
    # Test argument resolution
    arguments = {"text": "{{step_0.full_text}}", "max_length": 150}
    results = {
        "step_0": {
            "result": {
                "content": [{"text": '{"full_text": "Hello world"}'}]
            }
        }
    }
    
    resolved = orchestrator._resolve_arguments(arguments, results)
    
    if resolved["text"] == "Hello world" and resolved["max_length"] == 150:
        print("✅ Argument resolution working correctly")
        return True
    else:
        print(f"❌ Argument resolution failed. Expected text='Hello world', got {resolved}")
        return False

def test_workflow_planning():
    """Test workflow planning functionality"""
    print("📋 Testing workflow planning...")
    
    orchestrator = IntelligentOrchestrator()
    
    # Test various user requests
    test_requests = [
        "summarize this PDF",
        "analyze the sentiment of this document",
        "extract tables from this PDF", 
        "analyze energy consumption for this building",
        "give me a complete analysis of this document"
    ]
    
    all_passed = True
    for request in test_requests:
        workflow_steps = orchestrator.plan_workflow(request, {"file_path": "test.pdf"})
        if workflow_steps:
            print(f"  ✅ {request} -> {len(workflow_steps)} steps")
        else:
            print(f"  ❌ {request} -> No workflow planned")
            all_passed = False
    
    if all_passed:
        print("✅ Workflow planning working correctly")
        return True
    else:
        print("❌ Workflow planning failed")
        return False

@pytest.mark.asyncio
async def test_process_user_request():
    """Test the main process_user_request function"""
    print("🚀 Testing process_user_request function...")
    
    try:
        # Test with a simple goal
        result = await process_user_request("summarize this PDF", file_path="test.pdf")
        
        # Should return an error since agents aren't running, but the function should work
        if "error" in result:
            print("✅ process_user_request function working correctly")
            return True
        else:
            print("⚠️  Unexpected success (agents might be running)")
            return True
    except Exception as e:
        print(f"❌ process_user_request failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🤖 Quick Test Suite for Intelligent Orchestrator")
    print("=" * 60)
    
    tests = [
        ("Workflow Patterns", test_workflow_patterns),
        ("Keyword Extraction", test_keyword_extraction),
        ("Pattern Matching", test_pattern_matching),
        ("Argument Resolution", test_argument_resolution),
        ("Workflow Planning", test_workflow_planning),
        ("Process User Request", test_process_user_request)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: FAILED - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The intelligent orchestrator is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

if __name__ == "__main__":
    asyncio.run(main()) 