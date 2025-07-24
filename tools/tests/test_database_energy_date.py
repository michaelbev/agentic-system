#!/usr/bin/env python3
"""
Test script to verify database querying for latest energy reading date
"""

import asyncio
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from redaptive.orchestration.engine import OrchestrationEngine
from redaptive.orchestration.matchers.keyword_matcher import KeywordMatcher
from redaptive.orchestration.planners.dynamic_planner import DynamicPlanner

async def test_database_energy_date():
    """Test that energy-specific date queries correctly query the database"""
    
    print("🧪 Testing Database Energy Date Query")
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
        result = await engine.execute_workflow("test_database_energy_date_workflow", workflow)
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
                    
                    # Special handling for latest energy reading results (database format)
                    if 'usage_id' in result_data or ('meter_id' in result_data and 'timestamp' in result_data and 'energy_kwh' in result_data):
                        print(f"      🔌 Latest Energy Reading (Database):")
                        if 'usage_id' in result_data:
                            print(f"        • Usage ID: {result_data['usage_id']}")
                        if 'meter_id' in result_data:
                            print(f"        • Meter ID: {result_data['meter_id']}")
                        if 'building_id' in result_data:
                            print(f"        • Building ID: {result_data['building_id']}")
                        if 'timestamp' in result_data:
                            print(f"        • Reading Date: {result_data['timestamp']}")
                        if 'energy_type' in result_data:
                            print(f"        • Energy Type: {result_data['energy_type']}")
                        if 'energy_kwh' in result_data:
                            print(f"        • Energy Consumption: {result_data['energy_kwh']} kWh")
                        if 'energy_cost' in result_data:
                            print(f"        • Energy Cost: ${result_data['energy_cost']}")
                        if 'power_kw' in result_data:
                            print(f"        • Demand: {result_data['power_kw']} kW")
                        if 'power_factor' in result_data:
                            print(f"        • Power Factor: {result_data['power_factor']}")
                        if 'temperature_f' in result_data:
                            print(f"        • Temperature: {result_data['temperature_f']}°F")
                        if 'occupancy_percentage' in result_data:
                            print(f"        • Occupancy: {result_data['occupancy_percentage']}%")
                        if 'meter_type' in result_data:
                            print(f"        • Meter Type: {result_data['meter_type']}")
                        
                        # Check if the date matches the expected max date
                        if 'timestamp' in result_data:
                            reading_date = result_data['timestamp']
                            print(f"\n🎯 Database Query Result:")
                            print(f"        • Latest reading date from database: {reading_date}")
                            print(f"        • Expected max date: 2025-07-14 00:00:00.000")
                            
                            if "2025-07-14" in reading_date:
                                print(f"        ✅ CORRECT: Database query returned the expected latest date!")
                            else:
                                print(f"        ❌ INCORRECT: Database query returned {reading_date}, expected 2025-07-14")
                    
                    # Special handling for energy monitoring results (old format)
                    elif 'processed_readings' in result_data or 'meter_readings' in result_data:
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
    await test_database_energy_date()

if __name__ == "__main__":
    asyncio.run(main()) 