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
sys.path.insert(0, str(project_root))

from orchestration.intelligent.intelligent_orchestrator import IntelligentOrchestrator, process_user_request

async def main():
    """Run PDF processing orchestration example"""
    
    # Initialize the orchestrator
    orchestrator = IntelligentOrchestrator()
    
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