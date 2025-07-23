#!/usr/bin/env python3
"""
Utility Bill Processing Example - Redaptive Energy-as-a-Service Platform

This example demonstrates how to use the document processing agent
to process utility bills, ESG reports, and energy certificates.

Key capabilities demonstrated:
- Utility bill text extraction and processing
- ESG report data extraction
- Energy certificate processing
- Document analysis and validation
- Multi-format document support
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from orchestration.intelligent.intelligent_orchestrator import IntelligentOrchestrator

def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"📄 {title}")
    print(f"{'='*60}")

def print_section(title: str):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 50)

async def run_document_processing_examples():
    """Run document processing examples using the Document Processing Agent"""
    
    print_header("Redaptive Document Processing Examples")
    print("This example demonstrates automated document processing")
    print("for utility bills, ESG reports, and energy certificates.")
    
    # Initialize the orchestrator
    orchestrator = IntelligentOrchestrator()
    
    # Example 1: Utility Bill Processing
    print_section("Example 1: Utility Bill Processing")
    print("📝 Processing utility bills to extract key energy data")
    print("   The system will:")
    print("   1. Extract text from utility bill documents")
    print("   2. Parse energy consumption and cost data")
    print("   3. Validate data consistency")
    print("   4. Structure data for analysis")
    
    request1 = "process utility bill document for building B001 electricity charges"
    try:
        result1 = await orchestrator.execute_intelligent_workflow(request1)
        print(f"\n📊 Utility Bill Processing Results:")
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
    
    # Example 2: ESG Report Processing
    print_section("Example 2: ESG Report Data Extraction")
    print("📝 Extracting sustainability metrics from ESG reports")
    print("   The system will:")
    print("   1. Parse ESG report documents")
    print("   2. Extract carbon emissions data")
    print("   3. Identify sustainability KPIs")
    print("   4. Validate metric calculations")
    
    request2 = "extract ESG metrics from sustainability report including carbon footprint data"
    try:
        result2 = await orchestrator.execute_intelligent_workflow(request2)
        print(f"\n🌿 ESG Report Processing Results:")
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
    
    # Example 3: Energy Certificate Processing
    print_section("Example 3: Energy Certificate Extraction")
    print("📝 Processing energy efficiency certificates")
    print("   The system will:")
    print("   1. Extract certificate details")
    print("   2. Parse efficiency ratings")
    print("   3. Validate compliance data")
    print("   4. Structure certification information")
    
    request3 = "extract energy certificate data including ENERGY STAR ratings and compliance status"
    try:
        result3 = await orchestrator.execute_intelligent_workflow(request3)
        print(f"\n🏆 Certificate Processing Results:")
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
    
    # Example 4: Document Table Extraction
    print_section("Example 4: Document Table Data Extraction")
    print("📝 Extracting structured data from document tables")
    print("   The system will:")
    print("   1. Identify tables in documents")
    print("   2. Extract tabular data")
    print("   3. Structure table information")
    print("   4. Validate data relationships")
    
    request4 = "extract table data from energy report showing monthly consumption by meter"
    try:
        result4 = await orchestrator.execute_intelligent_workflow(request4)
        print(f"\n📊 Table Extraction Results:")
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
    
    # Example 5: Form Data Processing
    print_section("Example 5: Energy Form Data Processing")
    print("📝 Processing structured energy forms and applications")
    print("   The system will:")
    print("   1. Extract form field data")
    print("   2. Validate form completeness")
    print("   3. Structure form responses")
    print("   4. Process submission data")
    
    request5 = "process energy audit application form extracting all facility and contact information"
    try:
        result5 = await orchestrator.execute_intelligent_workflow(request5)
        print(f"\n📝 Form Processing Results:")
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
    
    # Example 6: Document Analysis
    print_section("Example 6: Comprehensive Document Analysis")
    print("📝 Performing comprehensive analysis of energy documents")
    print("   The system will:")
    print("   1. Analyze document content")
    print("   2. Extract key insights")
    print("   3. Identify important metrics")
    print("   4. Generate analysis summary")
    
    request6 = "analyze energy efficiency report document and extract key performance insights"
    try:
        result6 = await orchestrator.execute_intelligent_workflow(request6)
        print(f"\n🔍 Document Analysis Results:")
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
    print_header("Document Processing Summary")
    print("✅ Demonstrated 6 core document processing capabilities:")
    print("   1. 📄 Utility bill processing and data extraction")
    print("   2. 🌿 ESG report metrics extraction")
    print("   3. 🏆 Energy certificate processing")
    print("   4. 📊 Document table data extraction")
    print("   5. 📝 Energy form data processing")
    print("   6. 🔍 Comprehensive document analysis")
    print("\n📋 Ready for automated document processing at enterprise scale!")

if __name__ == "__main__":
    print("🚀 Document Processing Agent Examples")
    print("============================================================")
    print("This example demonstrates intelligent document processing")
    print("for Redaptive's AI-powered Energy-as-a-Service platform.")
    print("============================================================")
    
    asyncio.run(run_document_processing_examples())