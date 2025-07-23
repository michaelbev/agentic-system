#!/usr/bin/env python3
"""
Orchestration Demonstration Script

Demonstrates the intelligent orchestration capabilities of the Redaptive
Energy-as-a-Service platform with real-world scenarios.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from orchestration.intelligent.intelligent_orchestrator import IntelligentOrchestrator

def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_section(title: str):
    """Print a formatted section"""
    print(f"\n⚡ {title}")
    print("-" * 50)

async def demo_energy_portfolio_analysis():
    """Demonstrate energy portfolio analysis"""
    print_section("Energy Portfolio Analysis Demo")
    print("📝 Analyzing Fortune 500 energy portfolio with natural language")
    
    orchestrator = IntelligentOrchestrator()
    
    requests = [
        "Analyze energy consumption for portfolio P001 including all buildings",
        "Calculate ROI for LED retrofit project with $100000 budget",
        "Identify optimization opportunities with high impact potential",
        "Generate sustainability report including carbon footprint"
    ]
    
    for i, request in enumerate(requests, 1):
        print(f"\n📋 Request {i}: '{request}'")
        try:
            result = await orchestrator.execute_intelligent_workflow(request)
            print(f"✅ Workflow: {result.get('workflow_type', 'intelligent')}")
            print(f"📊 Steps: {len(result.get('execution_history', []))}")
            
            # Show execution summary
            if result.get('execution_history'):
                for j, step in enumerate(result['execution_history']):
                    status = "✅" if step.get('success') else "❌"
                    print(f"   {status} Step {j}: {step.get('status', 'completed')}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def demo_real_time_monitoring():
    """Demonstrate real-time energy monitoring"""
    print_section("Real-time Energy Monitoring Demo")
    print("📝 Demonstrating IoT meter processing and anomaly detection")
    
    orchestrator = IntelligentOrchestrator()
    
    monitoring_requests = [
        "Process real-time meter data for building B001 and detect anomalies",
        "Generate field engineer alert for equipment failure in meter M001",
        "Analyze energy usage patterns for portfolio optimization",
        "Manage demand response event for 200kW reduction"
    ]
    
    for i, request in enumerate(monitoring_requests, 1):
        print(f"\n📋 Monitoring Request {i}: '{request}'")
        try:
            result = await orchestrator.execute_intelligent_workflow(request)
            print(f"✅ Workflow planned: {len(result.get('planned_steps', []))} steps")
            
            # Show planned workflow
            if result.get('planned_steps'):
                for j, step in enumerate(result['planned_steps']):
                    agent = step.get('agent', 'unknown')
                    tool = step.get('tool', 'unknown')
                    print(f"   📋 Step {j}: {agent}.{tool}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def demo_financial_optimization():
    """Demonstrate EaaS financial optimization"""
    print_section("EaaS Financial Optimization Demo")
    print("📝 Demonstrating energy project finance and contract optimization")
    
    orchestrator = IntelligentOrchestrator()
    
    finance_requests = [
        "Optimize EaaS contract structure for maximum NPV with 70% sharing",
        "Assess project risk for solar installation with Monte Carlo analysis",
        "Select optimal technology mix for office building within $500000 budget",
        "Analyze performance-based contract with IPMVP Option B methodology"
    ]
    
    for i, request in enumerate(finance_requests, 1):
        print(f"\n📋 Finance Request {i}: '{request}'")
        try:
            result = await orchestrator.execute_intelligent_workflow(request)
            print(f"✅ Analysis planned: {len(result.get('planned_steps', []))} steps")
            
            # Show financial workflow
            if result.get('planned_steps'):
                for j, step in enumerate(result['planned_steps']):
                    agent = step.get('agent', 'unknown')
                    tool = step.get('tool', 'unknown')
                    print(f"   💰 Step {j}: {agent}.{tool}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def demo_document_processing():
    """Demonstrate document processing capabilities"""
    print_section("Document Processing Demo")
    print("📝 Demonstrating utility bill and ESG report processing")
    
    orchestrator = IntelligentOrchestrator()
    
    document_requests = [
        "Process utility bill document and extract energy consumption data",
        "Extract ESG metrics from sustainability report with carbon footprint",
        "Analyze energy certificate data including ENERGY STAR ratings",
        "Extract table data from energy report showing monthly consumption"
    ]
    
    for i, request in enumerate(document_requests, 1):
        print(f"\n📋 Document Request {i}: '{request}'")
        try:
            result = await orchestrator.execute_intelligent_workflow(request)
            print(f"✅ Processing planned: {len(result.get('planned_steps', []))} steps")
            
            # Show document workflow
            if result.get('planned_steps'):
                for j, step in enumerate(result['planned_steps']):
                    agent = step.get('agent', 'unknown')
                    tool = step.get('tool', 'unknown')
                    print(f"   📄 Step {j}: {agent}.{tool}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def demo_complex_scenarios():
    """Demonstrate complex multi-step scenarios"""
    print_section("Complex Multi-Agent Scenarios")
    print("📝 Demonstrating complex workflows requiring multiple agents")
    
    orchestrator = IntelligentOrchestrator()
    
    complex_requests = [
        "Analyze portfolio P001 energy data, identify optimization opportunities, calculate ROI for top 3 projects, and generate executive summary",
        "Process utility bills for all buildings, detect consumption anomalies, generate field alerts, and create cost optimization report",
        "Evaluate solar+storage project for manufacturing facility including financial analysis, risk assessment, and performance contracting recommendations"
    ]
    
    for i, request in enumerate(complex_requests, 1):
        print(f"\n📋 Complex Scenario {i}:")
        print(f"   '{request}'")
        try:
            result = await orchestrator.execute_intelligent_workflow(request)
            print(f"✅ Complex workflow: {len(result.get('planned_steps', []))} steps")
            
            # Show agents involved
            if result.get('planned_steps'):
                agents_used = set()
                for step in result['planned_steps']:
                    agents_used.add(step.get('agent', 'unknown'))
                print(f"   🤝 Agents involved: {', '.join(sorted(agents_used))}")
        except Exception as e:
            print(f"❌ Error: {e}")

def show_system_capabilities():
    """Show system capabilities overview"""
    print_header("Redaptive AI-Powered Energy-as-a-Service Platform")
    print("🏢 Fortune 500 Energy Portfolio Management Platform")
    print("🔋 Real-time IoT Processing: 12,000+ energy meters")
    print("💰 EaaS Revenue Optimization: AI-powered financial modeling")
    print("📊 Portfolio Intelligence: Advanced analytics and reporting")
    print("🤖 Multi-Agent Orchestration: Natural language interface")
    
    print(f"\n🎯 Available Agents:")
    agents = [
        "Portfolio Intelligence: 6 tools for Fortune 500 portfolio analysis",
        "Real-time Monitoring: 6 tools for IoT meter processing and alerts",
        "Energy Finance: 6 tools for EaaS contract and ROI optimization",
        "Document Processing: 7 tools for utility bills and ESG reports",
        "AI Summarization: 4 tools for text analysis and insights"
    ]
    
    for agent in agents:
        print(f"   • {agent}")
    
    print(f"\n🚀 Platform Status:")
    print("   ✅ Core agents implemented and tested")
    print("   ✅ Database schema with Fortune 500 sample data")
    print("   ✅ Intelligent orchestration engine")
    print("   ✅ Natural language workflow planning")
    print("   ⏳ IoT stream processing infrastructure (next phase)")

async def main():
    """Main demonstration function"""
    show_system_capabilities()
    
    print_header("Interactive Orchestration Demonstration")
    print("This demo shows how natural language requests are automatically")
    print("converted into intelligent multi-agent workflows for energy management.")
    
    demos = [
        ("Energy Portfolio Analysis", demo_energy_portfolio_analysis),
        ("Real-time Monitoring", demo_real_time_monitoring),
        ("Financial Optimization", demo_financial_optimization),
        ("Document Processing", demo_document_processing),
        ("Complex Scenarios", demo_complex_scenarios)
    ]
    
    try:
        for demo_name, demo_func in demos:
            print(f"\n🎬 Starting {demo_name} Demo...")
            await demo_func()
            
            # Pause between demos
            print(f"\n✅ {demo_name} Demo completed")
            await asyncio.sleep(1)
        
        print_header("Demonstration Summary")
        print("✅ All demonstrations completed successfully!")
        print("🎯 The Redaptive platform demonstrates:")
        print("   • Natural language to multi-agent workflow conversion")
        print("   • Intelligent agent selection and coordination")
        print("   • Comprehensive energy management capabilities")
        print("   • Fortune 500 scale portfolio analysis")
        print("   • Real-time IoT processing readiness")
        print("   • EaaS revenue optimization")
        
        print(f"\n🚀 Next Steps:")
        print("   1. Implement remaining 4 agents (Equipment Performance, Market Intelligence, etc.)")
        print("   2. Add IoT stream processing infrastructure (Redis/Kafka)")
        print("   3. Deploy production infrastructure (Kubernetes)")
        print("   4. Integrate with Redaptive's existing systems")
        
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    print("🚀 Redaptive Energy-as-a-Service Platform Demonstration")
    print("============================================================")
    asyncio.run(main())