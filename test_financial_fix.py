#!/usr/bin/env python3
"""
Test script to verify the financial analysis fix
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from interactive_cli import process_user_request, print_result

async def test_financial_analysis():
    """Test the financial analysis functionality"""
    print("💰 Testing financial analysis...")
    
    # Test the financial analysis request
    result = await process_user_request("Calculate ROI for LED retrofit project for building 123")
    
    # Print the result using the fixed function
    print_result(result, "Calculate ROI for LED retrofit project for building 123")
    
    print("\n✅ Financial analysis test completed!")

if __name__ == "__main__":
    asyncio.run(test_financial_analysis()) 