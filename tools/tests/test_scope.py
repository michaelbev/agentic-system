#!/usr/bin/env python3
"""
Test script to demonstrate scope detection functionality
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from interactive_cli import process_user_request

async def test_scope_detection():
    """Test the scope detection functionality"""
    print("🎯 Testing Scope Detection")
    print("=" * 50)
    
    # Test different types of requests
    test_requests = [
        # In-scope requests
        "What is the current date?",
        "Analyze energy consumption for building 123",
        "Calculate ROI for LED retrofit project",
        
        # Out-of-scope requests
        "Who was the first president of the United States?",
        "What's the weather like today?",
        "Who won the Super Bowl last year?",
        "Tell me about the history of Rome",
        "What's the latest news about politics?",
        "How do I make a chocolate cake?",
        "What's the capital of France?"
    ]
    
    for request in test_requests:
        print(f"\n🎯 Testing: '{request}'")
        result = await process_user_request(request)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Workflow: {result.get('workflow', 'Unknown')}")
            print(f"📋 Steps executed: {result.get('steps_executed', 0)}")
            
            if 'results' in result:
                for step_name, step_result in result['results'].items():
                    step_content = step_result.get('result', {}).get('content', [])
                    if step_content and len(step_content) > 0:
                        step_text = step_content[0].get('text', '')
                        try:
                            step_data = json.loads(step_text)
                            if isinstance(step_data, dict):
                                print(f"   ✅ {step_name}: Success")
                                # Show key data points
                                for key, value in step_data.items():
                                    if key in ['total_consumption', 'total_cost', 'portfolio_id', 'roi_percentage', 'facilities_found', 'summary_length']:
                                        print(f"      • {key}: {value}")
                                    elif key in ['current_date', 'current_time', 'timezone', 'day_of_week', 'analysis']:
                                        print(f"      • {key}: {value}")
                                    elif key in ['scope', 'system_domain', 'supported_topics', 'unsupported_topics', 'recommendation']:
                                        if key == 'supported_topics':
                                            print(f"      • {key}: {', '.join(value)}")
                                        elif key == 'unsupported_topics':
                                            print(f"      • {key}: {', '.join(value)}")
                                        else:
                                            print(f"      • {key}: {value}")
                                    elif isinstance(value, (int, float, str)) and len(str(value)) < 50:
                                        print(f"      • {key}: {value}")
                                if 'analysis' in step_data:
                                    print(f"      📝 Analysis: {step_data['analysis']}")
                        except:
                            print(f"   ✅ {step_name}: {step_text[:100]}...")
            
            if 'summary' in result:
                print(f"📝 Summary: {result['summary']}")
        
        print("-" * 50)

if __name__ == "__main__":
    import json
    asyncio.run(test_scope_detection()) 