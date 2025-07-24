#!/usr/bin/env python3
"""
Test script to demonstrate the date/time functionality
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from interactive_cli import process_user_request

async def test_time_functionality():
    """Test the time functionality"""
    print("🕐 Testing Date/Time Functionality")
    print("=" * 50)
    
    # Test different time-related requests
    test_requests = [
        "What is the current date?",
        "What time is it?",
        "Get the current time",
        "What day is today?",
        "Show me today's date"
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
                                # Show time-related data
                                for key, value in step_data.items():
                                    if key in ['current_date', 'current_time', 'timezone', 'day_of_week', 'analysis']:
                                        print(f"      • {key}: {value}")
                                    elif key == 'full_datetime':
                                        print(f"      • {key}: {value[:19]}...")
                                if 'analysis' in step_data:
                                    print(f"      📝 Analysis: {step_data['analysis']}")
                        except:
                            print(f"   ✅ {step_name}: {step_text[:100]}...")
            
            if 'summary' in result:
                print(f"📝 Summary: {result['summary']}")
        
        print("-" * 50)

if __name__ == "__main__":
    import json
    asyncio.run(test_time_functionality()) 