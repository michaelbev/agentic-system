#!/usr/bin/env python3
"""
Quick Demo - Simple Agent Usage
Shows how to use individual agents directly
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from redaptive.agents.energy import PortfolioIntelligenceAgent, EnergyMonitoringAgent

async def demo_portfolio_intelligence():
    """Demo Portfolio Intelligence Agent"""
    print("📊 Portfolio Intelligence Agent Demo")
    print("-" * 40)
    
    agent = PortfolioIntelligenceAgent()
    
    # Analyze portfolio energy usage
    result = await agent.analyze_portfolio_energy_usage(
        portfolio_id="demo_portfolio",
        date_range={
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
    )
    
    print("✅ Portfolio Analysis Result:")
    print(f"  Status: {result.get('result', {}).get('isError', False) and 'Error' or 'Success'}")
    if result.get('result', {}).get('content'):
        content = result['result']['content'][0]['text']
        print(f"  Data: {content[:100]}...")

async def demo_energy_monitoring():
    """Demo Energy Monitoring Agent"""
    print("\n⚡ Energy Monitoring Agent Demo")
    print("-" * 40)
    
    agent = EnergyMonitoringAgent()
    
    # Process meter data
    result = await agent.process_meter_data(
        meter_id="demo_meter_001",
        readings=[
            {
                "timestamp": "2024-01-01T12:00:00Z",
                "value": 150.5,
                "unit": "kWh"
            }
        ]
    )
    
    print("✅ Meter Data Processing Result:")
    print(f"  Status: {result.get('result', {}).get('isError', False) and 'Error' or 'Success'}")
    if result.get('result', {}).get('content'):
        content = result['result']['content'][0]['text']
        print(f"  Data: {content[:100]}...")

async def main():
    """Run quick demo"""
    print("🚀 Quick Demo - Individual Agent Usage")
    print("=" * 50)
    
    await demo_portfolio_intelligence()
    await demo_energy_monitoring()
    
    print("\n✨ Quick Demo Complete!")
    print("💡 The agents connect to a PostgreSQL database with energy schemas")
    print("📋 Each agent provides specialized tools for energy operations")

if __name__ == "__main__":
    asyncio.run(main())