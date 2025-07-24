#!/usr/bin/env python3
"""
Interactive CLI for Redaptive Agentic Platform
Send natural language prompts to the system and get responses
"""

import asyncio
import sys
import json
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration import OrchestrationEngine
from redaptive.agents import AGENT_REGISTRY

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
        matcher = KeywordMatcher()
        intent_result = await matcher.match_intent(user_request)
        
        # Step 2: Create workflow using the planner (handled by orchestration)
        planner = DynamicPlanner()
        workflow_plan = await planner.create_workflow(user_request, agent_names)
        
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
                "results": workflow_result["results"]
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
    
    # Print step-by-step results
    if 'results' in result:
        print("\n🔄 Step-by-step execution:")
        for step_name, step_data in result['results'].items():
            if isinstance(step_data, dict):
                # Check if result is directly available (system agent format)
                if 'result' in step_data and isinstance(step_data['result'], dict):
                    result_data = step_data['result']
                    print(f"   ✅ {step_name}: Success")
                    
                    # Show key data points
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
    print("Type 'quit' to exit, 'help' for commands")
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
                print("  • 'quit' - Exit the program")
                print("\n💡 Example requests:")
                print("  • 'Analyze energy consumption for building 123'")
                print("  • 'Calculate ROI for LED retrofit project'")
                print("  • 'Show me portfolio performance metrics'")
                print("  • 'Summarize this utility bill document'")
                print("  • 'Find optimization opportunities in our facilities'")
                continue
            elif not user_input:
                continue
            
            print(f"\n🔄 Processing: '{user_input}'")
            try:
                result = await process_user_request(user_input)
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