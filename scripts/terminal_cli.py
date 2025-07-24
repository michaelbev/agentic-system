#!/usr/bin/env python3
"""
Interactive CLI for Redaptive Agentic Platform
Send natural language prompts to the system and get responses
"""

import asyncio
import sys
import json
import os
from pathlib import Path

# Add src to path - now that we're in the scripts directory
src_dir = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration import OrchestrationEngine
from redaptive.agents import AGENT_REGISTRY

# Global flag for verbose logging
VERBOSE_LOGS = False

def toggle_verbose_logs():
    """Toggle verbose logging display"""
    global VERBOSE_LOGS
    VERBOSE_LOGS = not VERBOSE_LOGS
    return VERBOSE_LOGS

def print_log_header():
    """Print a collapsible log header"""
    if VERBOSE_LOGS:
        print("🔧 Initializing agents and services...")
        print("   (Type 'logs' to hide initialization details)")
    else:
        print("🔧 Initializing agents and services... (Type 'logs' to show details)")

def print_log_footer():
    """Print log footer"""
    if VERBOSE_LOGS:
        print("✅ All agents initialized successfully!")
    else:
        print("✅ Ready! All agents initialized.")

async def process_user_request(user_request: str, **context):
    """
    Process a user request using the orchestration engine.
    This fully delegates to the orchestration system for all logic.
    """
    try:
        # Initialize the orchestration engine
        engine = OrchestrationEngine()
        
        # Initialize all available agents
        agent_names = list(AGENT_REGISTRY.keys())
        success = await engine.initialize_agents(agent_names)
        
        if not success:
            return {
                "error": "Failed to initialize agents",
                "workflow": "user_request",
                "user_goal": user_request,
                "steps_executed": 0
            }
        
        # Delegate ALL logic to the orchestration system
        from redaptive.orchestration.matchers import KeywordMatcher
        from redaptive.orchestration.planners import DynamicPlanner
        
        # Step 1: Intent Matching (handled by orchestration)
        print_log_header()
        print("🔍 Step 1: Intent Matching")
        print("   Analyzing user request for intent...")
        
        matcher = KeywordMatcher()
        intent_result = await matcher.match_intent(user_request)
        
        print(f"   ✅ Intent: {intent_result['intent']}")
        print(f"   📊 Confidence: {intent_result.get('confidence', 0):.2f}")
        print(f"   💭 Reason: {intent_result.get('reason', 'No reason provided')}")
        
        # Step 2: Create workflow using the planner (handled by orchestration)
        print("\n⚙️  Step 2: Workflow Planning")
        print("   Creating workflow plan...")
        
        planner = DynamicPlanner()
        workflow_plan = await planner.create_workflow(user_request, agent_names)
        
        print(f"   ✅ Workflow ID: {workflow_plan.get('workflow_id', 'Unknown')}")
        method = workflow_plan.get('planning_method', 'unknown')
        method_display = "Rule-based" if method == "rule_based" else "Learning-based" if method == "learning_based" else method.upper()
        print(f"   🧠 Planning Method: {method_display}")
        print(f"   💭 Planning Reason: {workflow_plan.get('planning_reason', 'No reason provided')}")
        print(f"   📋 Steps Planned: {len(workflow_plan.get('steps', []))}")
        
        # Show workflow steps
        for i, step in enumerate(workflow_plan.get('steps', []), 1):
            agent = step.get('agent', 'Unknown')
            tool = step.get('tool', 'Unknown')
            print(f"   📝 Step {i}: {agent} → {tool}")
        
        print_log_footer()
        
        # Step 3: Execute the workflow (handled by orchestration)
        workflow_result = await engine.execute_workflow(
            workflow_plan["workflow_id"], 
            workflow_plan
        )
        
        # Step 4: Format the response based on orchestration results
        if workflow_result["status"] == "completed":
            return {
                "workflow": intent_result["intent"],
                "user_goal": user_request,
                "steps_executed": len(workflow_result["results"]),
                "summary": f"Processed {intent_result['intent']} request: {user_request}",
                "results": workflow_result["results"],
                "planning_method": workflow_plan.get("planning_method", "unknown"),
                "planning_reason": workflow_plan.get("planning_reason", "No planning reason provided")
            }
        else:
            return {
                "error": workflow_result.get("error", "Workflow execution failed"),
                "workflow": intent_result["intent"],
                "user_goal": user_request,
                "steps_executed": 0
            }
        
    except ImportError as e:
        if "psycopg2" in str(e):
            return {
                "error": "Database functionality disabled (psycopg2 not installed). Core functionality still available.",
                "workflow": "user_request",
                "user_goal": user_request,
                "steps_executed": 0,
                "suggestion": "Install psycopg2-binary to enable full database functionality"
            }
        else:
            return {
                "error": f"Import error: {str(e)}",
                "workflow": "user_request", 
                "user_goal": user_request,
                "steps_executed": 0
            }
    except Exception as e:
        return {
            "error": f"Failed to process request: {str(e)}",
            "workflow": "user_request",
            "user_goal": user_request,
            "steps_executed": 0
        }

def print_result(result, request):
    """Print the result in a formatted way"""
    print(f"\n📊 Results for: '{request}'")
    print("-" * 60)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        if 'suggestion' in result:
            print(f"💡 Suggestion: {result['suggestion']}")
        return
    
    # Print workflow info
    if 'workflow' in result:
        print(f"✅ Workflow: {result['workflow']}")
    if 'steps_executed' in result:
        print(f"📋 Steps executed: {result['steps_executed']}")
    
    # Print planning method info
    if 'planning_method' in result:
        method = result['planning_method']
        reason = result.get('planning_reason', 'No reason provided')
        
        if method == 'learning_based':
            print(f"🧠 Planning Method: Learning-based (AI-powered)")
        elif method == 'rule_based':
            print(f"🔧 Planning Method: Rule-based (Systematic)")
        else:
            print(f"❓ Planning Method: {method}")
        
        print(f"💭 Planning Reason: {reason}")
    
    # Print step-by-step results
    if 'results' in result:
        print("\n🔄 Step-by-step execution:")
        for step_name, step_data in result['results'].items():
            if isinstance(step_data, dict):
                # Check if result is directly available (system agent format)
                if 'result' in step_data and isinstance(step_data['result'], dict):
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
                    
                    # Special handling for latest energy reading results (database format)
                    elif 'usage_id' in result_data or ('meter_id' in result_data and 'timestamp' in result_data and 'energy_kwh' in result_data):
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
                    
                    # Show key data points for other types
                    else:
                        for key, value in result_data.items():
                            if key in ['total_consumption', 'total_cost', 'portfolio_id', 'roi_percentage', 'facilities_found', 'summary_length']:
                                print(f"      • {key}: {value}")
                            elif key in ['current_date', 'current_time', 'timezone', 'day_of_week', 'analysis']:
                                print(f"      • {key}: {value}")
                            elif key == 'full_datetime':
                                print(f"      • {key}: {value[:19]}...")  # Truncate long datetime
                            elif key in ['scope', 'system_domain', 'supported_topics', 'unsupported_topics', 'recommendation']:
                                if key == 'supported_topics':
                                    print(f"      • {key}: {', '.join(value)}")
                                elif key == 'unsupported_topics':
                                    print(f"      • {key}: {', '.join(value)}")
                                else:
                                    print(f"      • {key}: {value}")
                            elif key in ['status', 'error', 'message']:
                                if key == 'error':
                                    print(f"      ❌ {key}: {value}")
                                else:
                                    print(f"      • {key}: {value}")
                            elif key in ['financial_performance', 'contract_terms', 'optimized_contract']:
                                if isinstance(value, dict):
                                    print(f"      📊 {key}:")
                                    for sub_key, sub_value in value.items():
                                        if isinstance(sub_value, (int, float)):
                                            print(f"        - {sub_key}: {sub_value:,.2f}" if isinstance(sub_value, float) else f"        - {sub_key}: {sub_value}")
                                        else:
                                            print(f"        - {sub_key}: {sub_value}")
                                else:
                                    print(f"      • {key}: {value}")
                            elif isinstance(value, (int, float, str)) and len(str(value)) < 50:
                                print(f"      • {key}: {value}")
                            elif isinstance(value, dict) and len(str(value)) < 200:
                                print(f"      📋 {key}: {value}")
                    
                    # Show analysis if available
                    if 'analysis' in result_data:
                        print(f"      📝 Analysis: {result_data['analysis']}")
                    # Show recommendations if available
                    if 'recommendations' in result_data and isinstance(result_data['recommendations'], list):
                        print(f"      💡 Recommendations:")
                        for i, rec in enumerate(result_data['recommendations'][:3], 1):
                            print(f"        {i}. {rec}")
                
                # Handle legacy format with content array
                elif 'result' in step_data and 'content' in step_data['result']:
                    step_text = step_data['result']['content'][0].get('text', '{}')
                    if step_data.get('isError', False):
                        print(f"   ❌ {step_name}: Error - {step_text[:100]}...")
                    else:
                        try:
                            step_data_parsed = json.loads(step_text)
                            if isinstance(step_data_parsed, dict):
                                print(f"   ✅ {step_name}: Success")
                                # Show key data points
                                for key, value in step_data_parsed.items():
                                    if key in ['total_consumption', 'total_cost', 'portfolio_id', 'roi_percentage', 'facilities_found', 'summary_length']:
                                        print(f"      • {key}: {value}")
                                    elif key in ['current_date', 'current_time', 'timezone', 'day_of_week', 'analysis']:
                                        print(f"      • {key}: {value}")
                                    elif key == 'full_datetime':
                                        print(f"      • {key}: {value[:19]}...")  # Truncate long datetime
                                    elif key in ['scope', 'system_domain', 'supported_topics', 'unsupported_topics', 'recommendation']:
                                        if key == 'supported_topics':
                                            print(f"      • {key}: {', '.join(value)}")
                                        elif key == 'unsupported_topics':
                                            print(f"      • {key}: {', '.join(value)}")
                                        else:
                                            print(f"      • {key}: {value}")
                                    elif key in ['status', 'error', 'message']:
                                        if key == 'error':
                                            print(f"      ❌ {key}: {value}")
                                        else:
                                            print(f"      • {key}: {value}")
                                    elif key in ['financial_performance', 'contract_terms', 'optimized_contract']:
                                        if isinstance(value, dict):
                                            print(f"      📊 {key}:")
                                            for sub_key, sub_value in value.items():
                                                if isinstance(sub_value, (int, float)):
                                                    print(f"        - {sub_key}: {sub_value:,.2f}" if isinstance(sub_value, float) else f"        - {sub_key}: {sub_value}")
                                                else:
                                                    print(f"        - {sub_key}: {sub_value}")
                                        else:
                                            print(f"      • {key}: {value}")
                                    elif isinstance(value, (int, float, str)) and len(str(value)) < 50:
                                        print(f"      • {key}: {value}")
                                    elif isinstance(value, dict) and len(str(value)) < 200:
                                        print(f"      📋 {key}: {value}")
                                # Show analysis if available
                                if 'analysis' in step_data_parsed:
                                    print(f"      📝 Analysis: {step_data_parsed['analysis']}")
                                # Show recommendations if available
                                if 'recommendations' in step_data_parsed and isinstance(step_data_parsed['recommendations'], list):
                                    print(f"      💡 Recommendations:")
                                    for i, rec in enumerate(step_data_parsed['recommendations'][:3], 1):
                                        print(f"        {i}. {rec}")
                            else:
                                print(f"   ✅ {step_name}: {step_text[:100]}...")
                        except:
                            print(f"   ✅ {step_name}: {step_text[:100]}...")
                else:
                    print(f"   ✅ {step_name}: {str(step_data)[:100]}...")
    
    if 'summary' in result:
        print(f"\n📝 Summary: {result['summary']}")
    
    print("-" * 60)

async def interactive_mode():
    """Run the interactive CLI mode"""
    print("🚀 Redaptive Agentic Platform - Interactive CLI")
    print("=" * 60)
    print("Send natural language prompts to the system")
    print("Type 'quit' to exit, 'help' for commands, 'logs' to toggle verbose output")
    print("=" * 60)
    
    print(f"\n🤖 Available agents: {len(AGENT_REGISTRY)}")
    for agent_name in AGENT_REGISTRY.keys():
        print(f"  • {agent_name}")
    
    print("\n💡 Example prompts:")
    print("  • 'Analyze energy consumption for building 123'")
    print("  • 'Calculate ROI for LED retrofit project'")
    print("  • 'Show me portfolio performance metrics'")
    print("  • 'Summarize this utility bill document'")
    print("  • 'Find optimization opportunities in our facilities'")
    print("  • 'What is the current time?'")
    
    while True:
        try:
            print("\n" + "=" * 60)
            user_input = input("🎯 Enter your request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() in ['help', 'h']:
                print("\n📚 Available commands:")
                print("  • Natural language requests (e.g., 'analyze energy usage')")
                print("  • 'help' - Show this help")
                print("  • 'logs' - Toggle verbose initialization logs")
                print("  • 'quit' - Exit the program")
                print("\n💡 Example requests:")
                print("  • 'Analyze energy consumption for building 123'")
                print("  • 'Calculate ROI for LED retrofit project'")
                print("  • 'Show me portfolio performance metrics'")
                print("  • 'Summarize this utility bill document'")
                print("  • 'Find optimization opportunities in our facilities'")
                print("  • 'What is the current time?'")
                continue
            elif user_input.lower() in ['logs', 'log', 'verbose']:
                verbose = toggle_verbose_logs()
                print(f"🔧 Verbose logs {'enabled' if verbose else 'disabled'}")
                continue
            elif not user_input:
                continue
            
            print(f"\n🔄 Processing: '{user_input}'")
            print_log_header()
            
            try:
                result = await process_user_request(user_input)
                print_log_footer()
                print_result(result, user_input)
            except KeyboardInterrupt:
                print("\n⏹️  Request cancelled by user")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("💡 Try a simpler request or check if all dependencies are installed")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    """Main function"""
    await interactive_mode()

if __name__ == "__main__":
    asyncio.run(main()) 