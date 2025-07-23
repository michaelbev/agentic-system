#!/usr/bin/env python3
"""
Portfolio Analysis Example - Redaptive Energy-as-a-Service Platform

This example demonstrates how to use the portfolio intelligence agent
to analyze energy portfolios for Fortune 500 companies.

Key capabilities demonstrated:
- Portfolio-level energy analysis
- Optimization opportunity identification
- ROI calculations for energy projects
- Sustainability reporting
- Performance benchmarking
- Energy demand forecasting
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from orchestration.intelligent.intelligent_orchestrator import IntelligentOrchestrator

def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🏢 {title}")
    print(f"{'='*60}")

def print_section(title: str):
    """Print a formatted section"""
    print(f"\n⚡ {title}")
    print("-" * 50)

async def run_portfolio_analysis_examples():
    """Run portfolio analysis examples using the Portfolio Intelligence Agent"""
    
    print_header("Redaptive Portfolio Intelligence Examples")
    print("This example demonstrates Fortune 500 energy portfolio analysis")
    print("using the Portfolio Intelligence Agent with 6 specialized tools.")
    
    # Initialize the orchestrator
    orchestrator = IntelligentOrchestrator()
    
    # Example 1: Portfolio Energy Analysis
    print_section("Example 1: Portfolio Energy Usage Analysis")
    print("📝 Analyzing energy usage across a Fortune 500 real estate portfolio")
    print("   The system will:")
    print("   1. Analyze energy consumption patterns")
    print("   2. Identify usage trends and anomalies") 
    print("   3. Calculate efficiency metrics")
    
    request1 = "analyze energy usage for portfolio P001 including all buildings"
    try:
        result1 = await orchestrator.execute_intelligent_workflow(request1)
        print(f"\n📊 Portfolio Analysis Results:")
        print(f"✅ Request: '{request1}'")
        print(f"🎯 Workflow: {result1.get('workflow_type', 'unknown')}")
        print(f"📋 Steps executed: {len(result1.get('execution_history', []))}")
        if result1.get('execution_history'):
            print(f"\n🔄 Step-by-step execution:")
            for i, step in enumerate(result1['execution_history']):
                status = "✅" if step.get('success') else "❌"
                print(f"   {status} step_{i}: {step.get('status', 'Unknown')}")
                if step.get('result') and len(str(step['result'])) < 200:
                    print(f"      • {step['result']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Optimization Opportunities
    print_section("Example 2: Energy Optimization Opportunities")
    print("📝 Identifying energy efficiency opportunities")
    print("   The system will:")
    print("   1. Scan portfolio for inefficiencies")
    print("   2. Prioritize opportunities by impact")
    print("   3. Estimate potential savings")
    
    request2 = "identify optimization opportunities for portfolio P001 with high impact potential"
    try:
        result2 = await orchestrator.execute_intelligent_workflow(request2)
        print(f"\n🎯 Optimization Results:")
        print(f"✅ Request: '{request2}'")
        print(f"🎯 Workflow: {result2.get('workflow_type', 'unknown')}")
        print(f"📋 Steps executed: {len(result2.get('execution_history', []))}")
        if result2.get('execution_history'):
            print(f"\n🔄 Step-by-step execution:")
            for i, step in enumerate(result2['execution_history']):
                status = "✅" if step.get('success') else "❌"
                print(f"   {status} step_{i}: {step.get('status', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: ROI Calculation
    print_section("Example 3: Energy Project ROI Analysis")
    print("📝 Calculating return on investment for energy projects")
    print("   The system will:")
    print("   1. Analyze project costs and benefits")
    print("   2. Calculate financial metrics (NPV, IRR, payback)")
    print("   3. Compare multiple project scenarios")
    
    request3 = "calculate ROI for LED retrofit project at building B001 with $50000 budget"
    try:
        result3 = await orchestrator.execute_intelligent_workflow(request3)
        print(f"\n💰 ROI Analysis Results:")
        print(f"✅ Request: '{request3}'")
        print(f"🎯 Workflow: {result3.get('workflow_type', 'unknown')}")
        print(f"📋 Steps executed: {len(result3.get('execution_history', []))}")
        if result3.get('execution_history'):
            print(f"\n🔄 Step-by-step execution:")
            for i, step in enumerate(result3['execution_history']):
                status = "✅" if step.get('success') else "❌"
                print(f"   {status} step_{i}: {step.get('status', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 4: Sustainability Reporting
    print_section("Example 4: ESG Sustainability Report Generation")
    print("📝 Generating comprehensive sustainability reports")
    print("   The system will:")
    print("   1. Aggregate environmental data")
    print("   2. Calculate carbon footprint metrics")
    print("   3. Generate executive-level ESG reports")
    
    request4 = "generate sustainability report for portfolio P001 including carbon footprint and ESG metrics"
    try:
        result4 = await orchestrator.execute_intelligent_workflow(request4)
        print(f"\n📈 Sustainability Report Results:")
        print(f"✅ Request: '{request4}'")
        print(f"🎯 Workflow: {result4.get('workflow_type', 'unknown')}")
        print(f"📋 Steps executed: {len(result4.get('execution_history', []))}")
        if result4.get('execution_history'):
            print(f"\n🔄 Step-by-step execution:")
            for i, step in enumerate(result4['execution_history']):
                status = "✅" if step.get('success') else "❌"
                print(f"   {status} step_{i}: {step.get('status', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 5: Performance Benchmarking
    print_section("Example 5: Portfolio Performance Benchmarking")
    print("📝 Benchmarking portfolio performance against industry standards")
    print("   The system will:")
    print("   1. Compare against ENERGY STAR benchmarks")
    print("   2. Identify top and bottom performers")
    print("   3. Provide improvement recommendations")
    
    request5 = "benchmark portfolio P001 performance against ENERGY STAR and industry standards"
    try:
        result5 = await orchestrator.execute_intelligent_workflow(request5)
        print(f"\n📊 Benchmarking Results:")
        print(f"✅ Request: '{request5}'")
        print(f"🎯 Workflow: {result5.get('workflow_type', 'unknown')}")
        print(f"📋 Steps executed: {len(result5.get('execution_history', []))}")
        if result5.get('execution_history'):
            print(f"\n🔄 Step-by-step execution:")
            for i, step in enumerate(result5['execution_history']):
                status = "✅" if step.get('success') else "❌"
                print(f"   {status} step_{i}: {step.get('status', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 6: Energy Demand Forecasting
    print_section("Example 6: Energy Demand Forecasting")
    print("📝 Forecasting future energy demand and costs")
    print("   The system will:")
    print("   1. Analyze historical consumption patterns")
    print("   2. Factor in growth and efficiency projects")
    print("   3. Predict future energy costs and demand")
    
    request6 = "forecast energy demand for portfolio P001 for next 12 months including seasonal variations"
    try:
        result6 = await orchestrator.execute_intelligent_workflow(request6)
        print(f"\n🔮 Forecasting Results:")
        print(f"✅ Request: '{request6}'")
        print(f"🎯 Workflow: {result6.get('workflow_type', 'unknown')}")
        print(f"📋 Steps executed: {len(result6.get('execution_history', []))}")
        if result6.get('execution_history'):
            print(f"\n🔄 Step-by-step execution:")
            for i, step in enumerate(result6['execution_history']):
                status = "✅" if step.get('success') else "❌"
                print(f"   {status} step_{i}: {step.get('status', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Summary
    print_header("Portfolio Intelligence Summary")
    print("✅ Demonstrated 6 core portfolio intelligence capabilities:")
    print("   1. ⚡ Portfolio energy usage analysis")
    print("   2. 🎯 Optimization opportunity identification")
    print("   3. 💰 Energy project ROI calculations")
    print("   4. 📈 ESG sustainability reporting")
    print("   5. 📊 Performance benchmarking")
    print("   6. 🔮 Energy demand forecasting")
    print("\n🏢 Ready for Fortune 500 scale energy portfolio management!")

if __name__ == "__main__":
    print("🚀 Portfolio Intelligence Agent Examples")
    print("============================================================")
    print("This example demonstrates intelligent portfolio analysis")
    print("for Redaptive's AI-powered Energy-as-a-Service platform.")
    print("============================================================")
    
    asyncio.run(run_portfolio_analysis_examples())