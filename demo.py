#!/usr/bin/env python3
"""
Redaptive Agentic Platform Demo
Showcases multi-agent orchestration for Energy-as-a-Service operations
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration import OrchestrationEngine
from redaptive.agents import AGENT_REGISTRY

async def demo_agent_initialization():
    """Demo 1: Agent Discovery and Initialization"""
    print("🔍 Demo 1: Agent Discovery & Initialization")
    print("-" * 50)
    
    print("Available agents:")
    for agent_name in AGENT_REGISTRY.keys():
        print(f"  • {agent_name}")
    
    # Initialize orchestration engine
    engine = OrchestrationEngine()
    
    # Initialize energy agents
    agent_names = ["portfolio-intelligence", "energy-monitoring"]
    success = await engine.initialize_agents(agent_names)
    
    if success:
        print(f"✅ Successfully initialized {len(engine.agents)} agents")
        for name in engine.agents.keys():
            print(f"  • {name}: Ready")
    else:
        print("❌ Failed to initialize agents")
    
    return engine

async def demo_workflow_execution(engine):
    """Demo 2: Multi-Agent Workflow Execution"""
    print("\n⚙️  Demo 2: Multi-Agent Workflow Execution")
    print("-" * 50)
    
    # Define a portfolio analysis workflow
    workflow = {
        "name": "Portfolio Energy Analysis",
        "steps": [
            {
                "agent": "portfolio-intelligence",
                "tool": "analyze_portfolio_energy_usage", 
                "parameters": {
                    "portfolio_id": "portfolio_001",
                    "date_range": {
                        "start_date": "2024-01-01",
                        "end_date": "2024-12-31"
                    }
                }
            },
            {
                "agent": "energy-monitoring",
                "tool": "detect_anomalies",
                "parameters": {
                    "meter_ids": ["meter_001", "meter_002"],
                    "threshold": 1.5
                }
            }
        ]
    }
    
    print(f"📋 Executing workflow: {workflow['name']}")
    print(f"📊 Steps: {len(workflow['steps'])}")
    
    try:
        result = await engine.execute_workflow("demo_workflow_001", workflow)
        
        print("✅ Workflow completed")
        print(f"📈 Status: {result.get('status', 'Unknown')}")
        print(f"🔢 Steps completed: {result.get('steps_completed', 0)}/{result.get('total_steps', 0)}")
        
        if result.get('results'):
            print("\n📋 Step Results:")
            for step_id, step_result in result['results'].items():
                print(f"  • {step_id}: {step_result.get('status', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")

async def demo_streaming_capabilities():
    """Demo 3: Real-time Streaming Capabilities"""
    print("\n📡 Demo 3: Real-time Data Streaming")
    print("-" * 50)
    
    try:
        from redaptive.streaming import StreamManager
        
        print("🌊 Stream Manager capabilities:")
        print("  • Real-time meter data processing (12,000+ meters)")
        print("  • 48k+ data points per hour capacity")
        print("  • Redis/Kafka integration support")
        print("  • Anomaly detection streaming")
        
        # Show configuration
        manager = StreamManager()
        print(f"✅ Stream Manager initialized")
        print(f"📊 Supported formats: {manager.get_supported_formats()}")
        
    except Exception as e:
        print(f"⚠️  Streaming demo limited: {e}")

async def demo_agent_capabilities():
    """Demo 4: Individual Agent Capabilities"""
    print("\n🤖 Demo 4: Agent Capabilities Overview")
    print("-" * 50)
    
    capabilities = {
        "portfolio-intelligence": [
            "Portfolio energy analysis",
            "Multi-building optimization", 
            "Strategic recommendations",
            "Financial performance tracking"
        ],
        "energy-monitoring": [
            "Real-time meter monitoring",
            "Anomaly detection",
            "Alert generation",
            "Data validation"
        ],
        "energy-finance": [
            "EaaS revenue optimization",
            "ROI analysis",
            "Cost-benefit modeling",
            "Financial reporting"
        ],
        "document-processing": [
            "PDF extraction",
            "Energy report analysis",
            "Contract processing",
            "Data extraction"
        ],
        "summarize": [
            "Content summarization",
            "Report generation",
            "Key insight extraction",
            "Executive summaries"
        ]
    }
    
    for agent_name, features in capabilities.items():
        print(f"\n🎯 {agent_name.title().replace('-', ' ')}:")
        for feature in features:
            print(f"  • {feature}")

async def demo_production_scale():
    """Demo 5: Production Scale Capabilities"""
    print("\n🏭 Demo 5: Production Scale Capabilities")
    print("-" * 50)
    
    print("📊 Platform Scale:")
    print("  • 12,000+ energy meters supported")
    print("  • 48,000+ data points/hour processing")
    print("  • Fortune 500 portfolio management")
    print("  • Multi-tenant EaaS operations")
    
    print("\n🔧 Technical Features:")
    print("  • Async multi-agent orchestration")
    print("  • PostgreSQL + Redis architecture") 
    print("  • MCP (Model Context Protocol) agents")
    print("  • Docker/Kubernetes deployment")
    
    print("\n🎯 Business Capabilities:")
    print("  • Energy portfolio optimization")
    print("  • Real-time monitoring & alerts")
    print("  • Financial optimization & ROI")
    print("  • Automated report generation")

async def main():
    """Run the complete demo"""
    print("🚀 Redaptive Agentic AI Platform Demo")
    print("=" * 60)
    print("Multi-Agent Energy-as-a-Service (EaaS) Platform")
    print("=" * 60)
    
    try:
        # Demo 1: Agent initialization
        engine = await demo_agent_initialization()
        
        # Demo 2: Workflow execution
        await demo_workflow_execution(engine)
        
        # Demo 3: Streaming capabilities  
        await demo_streaming_capabilities()
        
        # Demo 4: Agent capabilities
        await demo_agent_capabilities()
        
        # Demo 5: Production scale
        await demo_production_scale()
        
        print("\n✨ Demo Complete!")
        print("📚 Next steps:")
        print("  • Explore examples/ directory")
        print("  • Review docs/ for detailed guides")
        print("  • Check infrastructure/ for deployment")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())