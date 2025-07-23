#!/usr/bin/env python3
"""
Energy Analysis Orchestration Example
Demonstrates intelligent orchestration for energy consumption analysis

This example shows how the intelligent orchestration system:
1. Analyzes natural language requests
2. Plans appropriate workflows automatically
3. Executes multi-agent workflows
4. Provides structured results

The system transforms simple requests like "analyze energy consumption" 
into complex multi-step workflows involving energy data agents, analysis tools,
and reporting systems.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from redaptive.orchestration import OrchestrationEngine
from redaptive.agents import AGENT_REGISTRY

def explain_result(result, request, example_name):
    """
    Explain the orchestration result in a user-friendly way
    """
    print(f"\n📊 {example_name} Results:")
    print("-" * 50)
    
    if 'error' in result:
        print(f"❌ Workflow failed: {result['error']}")
        return
    
    print(f"✅ Request: '{request}'")
    print(f"🎯 Workflow: {result.get('workflow', 'Unknown')}")
    print(f"📋 Steps executed: {result.get('steps_executed', 0)}")
    
    # Show what each step did
    if 'results' in result:
        print("\n🔄 Step-by-step execution:")
        for step_name, step_result in result['results'].items():
            step_content = step_result.get('result', {}).get('content', [])
            if step_content and len(step_content) > 0:
                step_text = step_content[0].get('text', '')
                is_error = step_result.get('result', {}).get('isError', False)
                
                if is_error:
                    print(f"   ❌ {step_name}: Error - {step_text[:100]}...")
                else:
                    # Try to parse JSON response
                    try:
                        step_data = json.loads(step_text)
                        if isinstance(step_data, dict):
                            print(f"   ✅ {step_name}: Success")
                            # Show key data points
                            for key, value in step_data.items():
                                if key in ['total_consumption', 'total_cost', 'facility_id', 'service_type']:
                                    print(f"      • {key}: {value}")
                        else:
                            print(f"   ✅ {step_name}: {step_text[:100]}...")
                    except:
                        print(f"   ✅ {step_name}: {step_text[:100]}...")
    
    if 'summary' in result:
        print(f"\n📝 Summary: {result['summary']}")
    
    print("-" * 50)

async def main():
    """Run energy analysis orchestration example"""
    
    print("🚀 Energy Analysis Orchestration Example")
    print("=" * 60)
    print("This example demonstrates intelligent workflow orchestration")
    print("for energy-as-a-service operations using natural language requests.")
    print("=" * 60)
    
    # Example 1: Basic energy consumption analysis
    print("\n⚡ Example 1: Energy Data Analysis")
    print("📝 This example shows how to analyze energy consumption data")
    print("   The system will:")
    print("   1. Identify this as an energy analysis request")
    print("   2. Plan a workflow to fetch energy data")
    print("   3. Execute the workflow using the energy agent")
    
    request = "analyze energy consumption for this building"
    
    try:
        result = await process_user_request(
            request,
            facility_id="123",
            date_range={"start_date": "2024-01-01", "end_date": "2024-01-31"},
            energy_type="electricity"
        )
        explain_result(result, request, "Energy Data Analysis")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Service Booking
    print("\n📅 Example 2: Service Booking")
    print("📝 This example shows how to book energy services")
    print("   The system will:")
    print("   1. Recognize this as a service booking request")
    print("   2. Plan a workflow to book the service")
    print("   3. Execute booking using the energy agent")
    
    request = "schedule an energy audit for next week"
    
    try:
        result = await process_user_request(
            request,
            facility_id="456",
            service_type="Audit",
            service_date="2024-01-15",
            customer_name="John Doe",
            customer_email="john.doe@example.com"
        )
        explain_result(result, request, "Service Booking")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Facility Search
    print("\n🔍 Example 3: Facility Search")
    print("📝 This example shows how to search for energy facilities")
    print("   The system will:")
    print("   1. Recognize this as a facility search request")
    print("   2. Plan a workflow to search facilities")
    print("   3. Execute search using the energy agent")
    
    request = "find office buildings in Denver for energy services"
    
    try:
        result = await process_user_request(
            request,
            location="Denver",
            facility_type="office",
            min_capacity=5000
        )
        explain_result(result, request, "Facility Search")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 4: Multi-step Analysis
    print("\n📊 Example 4: Multi-step Energy Analysis")
    print("📝 This example shows complex multi-step workflows")
    print("   The system will:")
    print("   1. Analyze the comprehensive request")
    print("   2. Plan a multi-step workflow")
    print("   3. Execute data retrieval and analysis")
    
    request = "analyze energy consumption trends and provide efficiency recommendations"
    
    try:
        result = await process_user_request(
            request,
            facility_id="101",
            date_range={"start_date": "2024-01-01", "end_date": "2024-12-31"},
            energy_type="electricity"
        )
        explain_result(result, request, "Multi-step Energy Analysis")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 5: Summary and Insights
    print("\n🎯 Example 5: System Intelligence Summary")
    print("📝 This example demonstrates the system's intelligence")
    print("   Key features demonstrated:")
    print("   • Natural language understanding")
    print("   • Automatic workflow planning")
    print("   • Multi-agent coordination")
    print("   • Error handling and recovery")
    print("\n✨ The system transforms simple requests into complex workflows")
    print("   without requiring users to understand the underlying complexity.")

if __name__ == "__main__":
    asyncio.run(main())