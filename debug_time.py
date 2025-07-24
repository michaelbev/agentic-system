#!/usr/bin/env python3
"""
Debug script to test time request functionality
"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from interactive_cli import process_user_request

async def debug_time_request():
    """Debug the time request functionality"""
    print("🔍 Debugging time request...")
    
    # Test the time request
    result = await process_user_request("what is the current time")
    
    print("\n📊 Raw Result:")
    print(json.dumps(result, indent=2))
    
    print("\n🔍 Analysis:")
    if 'results' in result:
        for step_name, step_data in result['results'].items():
            print(f"\nStep: {step_name}")
            print(f"Step data type: {type(step_data)}")
            print(f"Step data keys: {list(step_data.keys()) if isinstance(step_data, dict) else 'Not a dict'}")
            
            if isinstance(step_data, dict) and 'result' in step_data:
                result_data = step_data['result']
                print(f"Result keys: {list(result_data.keys())}")
                
                if 'content' in result_data:
                    content = result_data['content']
                    print(f"Content type: {type(content)}")
                    print(f"Content length: {len(content)}")
                    
                    if content and len(content) > 0:
                        first_content = content[0]
                        print(f"First content keys: {list(first_content.keys())}")
                        
                        if 'text' in first_content:
                            text = first_content['text']
                            print(f"Text: {text}")
                            
                            try:
                                parsed = json.loads(text)
                                print(f"Parsed JSON keys: {list(parsed.keys())}")
                                print(f"Parsed data: {json.dumps(parsed, indent=2)}")
                            except:
                                print(f"Could not parse as JSON: {text}")

if __name__ == "__main__":
    asyncio.run(debug_time_request()) 