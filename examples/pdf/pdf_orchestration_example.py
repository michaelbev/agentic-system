#!/usr/bin/env python3
"""
PDF Processing Orchestration Example
Demonstrates intelligent orchestration for PDF document processing
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from redaptive.orchestration import OrchestrationEngine
from redaptive.agents import AGENT_REGISTRY

async def process_user_request(user_request: str, **context):
    """
    Process a user request using the orchestration engine.
    This is a simplified version that demonstrates the concept.
    """
    try:
        # Initialize the orchestration engine
        engine = OrchestrationEngine()
        
        # Initialize content processing agents
        agent_names = ["document-processing", "summarize"]
        success = await engine.initialize_agents(agent_names)
        
        if not success:
            return {
                "error": "Failed to initialize agents",
                "workflow": "pdf_processing",
                "user_goal": user_request,
                "steps_executed": 0
            }
        
        # For demo purposes, return a mock result
        # In a real implementation, this would analyze the request and execute workflows
        return {
            "workflow": "pdf_processing",
            "user_goal": user_request,
            "steps_executed": 2,
            "summary": f"Processed PDF request: {user_request}",
            "results": {
                "step_1": {
                    "agent": "document-processing",
                    "tool": "extract_text",
                    "result": {
                        "content": [{"text": "Extracted 1500 characters from PDF document"}],
                        "isError": False
                    }
                },
                "step_2": {
                    "agent": "summarize",
                    "tool": "summarize_text",
                    "result": {
                        "content": [{"text": "Generated 200 character summary of the document"}],
                        "isError": False
                    }
                }
            }
        }
        
    except Exception as e:
        return {
            "error": f"Failed to process request: {str(e)}",
            "workflow": "pdf_processing",
            "user_goal": user_request,
            "steps_executed": 0
        }

async def main():
    """Run PDF processing orchestration example"""
    
    # Initialize the orchestrator
    engine = OrchestrationEngine()
    
    print("🚀 PDF Processing Orchestration Example")
    print("=" * 50)
    
    # Example 1: Extract and summarize a PDF
    print("\n📄 Example 1: Extract and summarize PDF")
    print("-" * 40)
    
    request = "Extract text from the sample PDF and provide a summary"
    
    try:
        result = await process_user_request(request, file_path="tests/files/Inspirational Career Summary Report.pdf")
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Process multiple PDFs
    print("\n📚 Example 2: Process multiple PDFs")
    print("-" * 40)
    
    request = "Process all PDFs in the documents folder and create summaries"
    
    try:
        result = await process_user_request(request, file_path="tests/files/Inspirational Career Summary Report.pdf")
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Extract specific information
    print("\n🔍 Example 3: Extract specific information")
    print("-" * 40)
    
    request = "Extract all dates and amounts from the financial report PDF"
    
    try:
        result = await process_user_request(request, file_path="tests/files/Inspirational Career Summary Report.pdf")
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 