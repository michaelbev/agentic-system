#!/usr/bin/env python3
"""
Test script to verify the time request fix
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from interactive_cli import process_user_request, print_result

async def test_time_request():
    """Test the time request functionality"""
    print("🕐 Testing time request...")
    
    # Test the time request
    result = await process_user_request("what is the current time")
    
    # Print the result using the fixed function
    print_result(result, "what is the current time")
    
    print("\n✅ Time request test completed!")

if __name__ == "__main__":
    asyncio.run(test_time_request()) 