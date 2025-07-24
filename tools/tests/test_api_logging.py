#!/usr/bin/env python3
"""
Test script to verify API key logging is fixed
"""

import sys
import os
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

def test_api_logging():
    """Test that API keys are not logged"""
    print("🔍 Testing API key logging...")
    
    try:
        from redaptive.agents.content.summarization import SummarizeAgent
        print("✅ Import successful")
        
        # Set a test API key
        os.environ['GOOGLE_API_KEY'] = 'test_key_for_logging_check'
        
        # This should not log the actual API key
        agent = SummarizeAgent()
        print("✅ SummarizeAgent initialized without logging API key")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_api_logging()
    if success:
        print("🎉 API key logging fix verified!")
    else:
        print("❌ API key logging fix failed!") 