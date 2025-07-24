#!/usr/bin/env python3
"""Debug script for LLM client."""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners.llm_client import LLMClient

async def test_llm_client():
    """Test the LLM client directly."""
    
    client = LLMClient()
    
    test_queries = [
        "What is the date of the most recent energy usage reading?",
        "What's the current time?",
        "Calculate ROI for LED retrofit project",
        "Find energy optimization opportunities",
        "Who was the first president of the United States?"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        response = await client.generate(query)
        print(f"Response: {response[:200]}...")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_llm_client()) 