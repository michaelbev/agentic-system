#!/usr/bin/env python3
"""Demo script for LLM client functionality."""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent.parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners.llm_client import LLMClient

async def llm_client_demo():
    """Demonstrate LLM client functionality."""
    
    print("🧠 LLM Client Demo")
    print("=" * 40)
    
    # Environment check
    print("🔍 Environment Configuration:")
    print(f"  PREFERRED_LLM_PROVIDER: {os.getenv('PREFERRED_LLM_PROVIDER', 'Not set')}")
    print(f"  ANTHROPIC_API_KEY: {'✅ Set' if os.getenv('ANTHROPIC_API_KEY') else '❌ Not set'}")
    print(f"  OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
    print()
    
    # Test providers
    providers = ["anthropic", "openai"]
    
    for provider in providers:
        print(f"🔧 Testing {provider.upper()} provider:")
        try:
            client = LLMClient(provider=provider)
            print(f"  ✅ {provider.upper()} client initialized")
            
            # Test simple generation
            test_prompt = "Respond with just 'Test successful' if you can see this message."
            response = await client.generate(test_prompt)
            print(f"  📝 Response: {response[:100]}...")
            
        except Exception as e:
            print(f"  ❌ {provider.upper()} client error: {e}")
        
        print()
    
    print("✅ LLM client demo completed!")
    print("\n🎯 **Key Insights**:")
    print("  • LLM client supports multiple providers (Anthropic, OpenAI)")
    print("  • Graceful fallback to mock responses when API unavailable")
    print("  • Consistent interface across different providers")

if __name__ == "__main__":
    asyncio.run(llm_client_demo()) 