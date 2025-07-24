#!/usr/bin/env python3
"""
Test script to demonstrate CLI handling of energy-specific date queries
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from redaptive.orchestration.engine import OrchestrationEngine
from redaptive.orchestration.matchers.keyword_matcher import KeywordMatcher
from redaptive.orchestration.planners.dynamic_planner import DynamicPlanner

async def test_cli_energy_date():
    """Test CLI-style processing of energy-specific date queries"""
    
    print("🧪 Testing CLI Energy Date Query Processing")
    print("=" * 60)
    
    # Test query
    query = "what is the date of the most recent energy usage reading?"
    
    print(f"🎯 Query: '{query}'")
    print("-" * 40)
    
    # Initialize components
    matcher = KeywordMatcher()
    planner = DynamicPlanner()
    engine = OrchestrationEngine()
    
    # Initialize agents
    await engine.initialize_agents([
        "portfolio-intelligence",
        "energy-monitoring", 
        "energy-finance",
        "document-processing",
        "summarize",
        "system"
    ])
    
    print(f"✅ Initialized {len(engine.agents)} agents")
    
    # Test intent matching
    intent_result = await matcher.match_intent(query)
    print(f"🎯 Intent: {intent_result['intent']} (confidence: {intent_result['confidence']:.2f})")
    print(f"📝 Reason: {intent_result.get('reason', 'N/A')}")
    
    # Test workflow planning
    workflow = await planner.create_workflow(query, list(engine.agents.keys()))
    print(f"📋 Workflow: {workflow['workflow_id']}")
    
    # Show workflow steps
    for j, step in enumerate(workflow['steps'], 1):
        print(f"  Step {j}: {step['agent']} -> {step['tool']}")
    
    # Test execution
    try:
        result = await engine.execute_workflow("test_energy_date_workflow", workflow)
        print(f"✅ Execution successful")
        
        # Display results in CLI format
        print(f"\n📊 Results for: '{query}'")
        print("-" * 60)
        
        if 'results' in result:
            print("\n🔄 Step-by-step execution:")
            for step_name, step_data in result['results'].items():
                if isinstance(step_data, dict) and 'result' in step_data:
                    result_data = step_data['result']
                    print(f"   ✅ {step_name}: Success")
                    
                    # Special handling for energy monitoring results
                    if 'processed_readings' in result_data or 'meter_readings' in result_data:
                        print(f"      🔌 Energy Monitoring Data:")
                        if 'processed_readings' in result_data:
                            print(f"        • Processed readings: {result_data['processed_readings']}")
                        if 'total_readings' in result_data:
                            print(f"        • Total readings: {result_data['total_readings']}")
                        if 'processing_rate' in result_data:
                            print(f"        • Processing rate: {result_data['processing_rate']}")
                        if 'anomalies_detected' in result_data:
                            print(f"        • Anomalies detected: {result_data['anomalies_detected']}")
                        if 'alerts_generated' in result_data:
                            print(f"        • Alerts generated: {result_data['alerts_generated']}")
                        if 'timestamp' in result_data:
                            print(f"        • Latest reading timestamp: {result_data['timestamp']}")
                        
                        # Show details if available
                        if 'details' in result_data and isinstance(result_data['details'], dict):
                            details = result_data['details']
                            if 'processing_summary' in details:
                                summary = details['processing_summary']
                                if 'meters_processed' in summary:
                                    print(f"        • Meters processed: {summary['meters_processed']}")
                                if 'time_span' in summary:
                                    print(f"        • Time span: {summary['time_span']}")
                                if 'data_quality' in summary:
                                    print(f"        • Data quality: {summary['data_quality']}")
                        
                        # Show meter readings if available
                        if 'meter_readings' in result_data and isinstance(result_data['meter_readings'], list):
                            readings = result_data['meter_readings']
                            if readings:
                                latest_reading = readings[0]  # Most recent reading
                                print(f"        📊 Latest Reading:")
                                print(f"          - Meter ID: {latest_reading.get('meter_id', 'N/A')}")
                                print(f"          - Timestamp: {latest_reading.get('timestamp', 'N/A')}")
                                print(f"          - Energy (kWh): {latest_reading.get('energy_kwh', 'N/A')}")
                                print(f"          - Power (kW): {latest_reading.get('power_kw', 'N/A')}")
                                if 'temperature' in latest_reading:
                                    print(f"          - Temperature: {latest_reading['temperature']}°C")
        
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Execution failed: {e}")

async def main():
    """Main test function"""
    await test_cli_energy_date()

if __name__ == "__main__":
    asyncio.run(main()) 