#!/usr/bin/env python3
"""
Test Multi-Agent PDF Summary Workflow
Demonstrates extracting text from PDF and generating a summary using multiple agents
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the path
src_dir = str(Path(__file__).parent.parent.parent / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from redaptive.orchestration import OrchestrationEngine

async def test_pdf_summary_workflow():
    """Test the PDF extraction and summarization workflow"""
    print("🚀 Testing Intelligent Multi-Agent PDF Summary Workflow")
    print("=" * 60)
    
    # Path to the PDF file
    pdf_path = "files/Inspirational Career Summary Report.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        print("💡 Make sure the PDF file exists in the tests directory")
        return
    
    print(f"📄 Processing PDF: {pdf_path}")
    
    orchestrator = OrchestrationEngine()
    
    try:
        # Test the PDF extraction and summarization workflow
        print("\n🔄 Starting PDF extraction and summarization...")
        
        # Use the intelligent workflow composition
        result = await orchestrator.execute_workflow("test_workflow", {
            "summarize this PDF",
            file_path=pdf_path,
            max_length=200
        )
        
        if "error" in result:
            print(f"❌ Workflow failed: {result['error']}")
            return
        
        # Display results
        print("\n✅ PDF Summary Workflow Completed Successfully!")
        print("=" * 60)
        
        print(f"📄 PDF File: {pdf_path}")
        print(f"📊 Workflow Steps: {result['steps_executed']}")
        print(f"📝 Workflow Summary: {result['summary']}")
        
        # Extract and display the results from each step
        if 'results' in result:
            print("\n📋 WORKFLOW RESULTS:")
            print("-" * 40)
            
            for step_id, step_result in result['results'].items():
                print(f"\n🔹 {step_id}:")
                if "result" in step_result and "content" in step_result["result"]:
                    content = step_result["result"]["content"][0]["text"]
                    try:
                        data = json.loads(content)
                        if "full_text" in data:
                            print(f"   📄 Extracted {len(data['full_text'])} characters")
                            preview = data['full_text'][:300] + "..." if len(data['full_text']) > 300 else data['full_text']
                            print(f"   📝 Preview: {preview}")
                        elif "summary" in data:
                            print(f"   📝 Summary: {data['summary']}")
                        else:
                            print(f"   📊 Data: {json.dumps(data, indent=2)}")
                    except:
                        print(f"   📄 Raw content: {content[:200]}...")
                else:
                    print(f"   ⚠️  Unexpected result format: {step_result}")
        
        print("\n🔍 WORKFLOW DETAILS:")
        print("-" * 40)
        print(f"🎯 User Goal: {result['user_goal']}")
        print(f"📋 Workflow Type: {result['workflow']}")
            
    except Exception as e:
        print(f"❌ Error during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n🧹 Cleaning up...")
        try:
            await orchestrator.stop_all_agents()
            print("✅ Cleanup completed")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
            print("✅ Test completed (cleanup had issues)")

async def test_simple_summary():
    """Test a simple text summarization without PDF extraction"""
    print("\n🔧 Testing Simple Text Summarization")
    print("=" * 50)
    
    orchestrator = OrchestrationEngine()
    
    try:
        # Sample text about the PDF content
        sample_text = """
As you begin to think about your profile pattern and how it relates to your job search, you may want to 
consider how your profile pattern may affect your level of success and satisfaction in your next position and 
how you approach the interview.   
 
Factors to Consider When Evaluating a New Position 
 
•  Inspirational people are often self-starters and results oriented.  They often prefer positions that 
allow them to quickly advance in an organization.  They typically enjoy solving difficult problems 
and overcoming major obstacles.  A position where they can be bold and adventurous, explore the 
unknown, or try the untried is usually preferred.   
 
•  They usually prefer positions that allow them to interact positively with other people.  They often 
excel in positions where persuasion to sell an idea, service or product is an essential skill.  
 
•  Inspirational people make friends with ease, create a sense of good will, and remain optimistic in the 
face of difficulty.  They prefer work environments that encourage these attributes and behaviors. 
 
•  They often prefer positions that frequently require them to be alert, quick on their feet, and to juggle 
different tasks at one time.  They thrive in positions where they can manage change quickly and 
effectively. 
 
•  Inspirational people often prefer positions with minimal boundaries and few rules to follow.  They 
like the freedom to set their own goals, take risks, and question the status quo. 
 
•  They are self-reliant, independent, and they are not afraid of being held accountable for their actions.  
They will perform best in positions where these traits and performance measures are present and 
encouraged. 
 
Interview Considerations 
 
Consider these questions below as you evaluate whether the position and company are right for you: 
 
•  Does this position allow me growth opportunity into a leadership role? 
•  What is the process for making decisions? 
•  What are my manager's expectations of me in the first 90 days? 
•  Does the company reward and encourage creativity and independence?  
•  Who will be giving me direction, and how will I be involved in defining my goals and objectives? 
•  How often are performance evaluations administered, and what are the key performance metrics? 
        """
        
        print("📝 Sample text to summarize:")
        print(sample_text.strip())
        
        result = await orchestrator.execute_workflow("test_workflow", {
            "summarize this text",
            text=sample_text,
            max_length=100
        )
        
        if "error" in result:
            print(f"❌ Summarization failed: {result['error']}")
            return
        
        # Handle the new intelligent workflow result format
        if "results" in result:
            # Get the last step result (summarization)
            last_step = f"step_{result['steps_executed'] - 1}"
            if last_step in result["results"]:
                step_result = result["results"][last_step]
                if "result" in step_result and "content" in step_result["result"]:
                    summary_content = step_result["result"]["content"][0]["text"]
                    summary_data = json.loads(summary_content)
                    
                    print("\n📝 Generated Summary:")
                    print("-" * 30)
                    print(summary_data.get('summary', 'No summary generated'))
                else:
                    print("\n📝 Summary result not found in expected format")
            else:
                print("\n📝 Summary step not found")
        else:
            print("\n📝 No results found in workflow response")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        try:
            await orchestrator.stop_all_agents()
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")

async def main():
    """Run the PDF summary workflow test"""
    print("🎯 Multi-Agent PDF Summary Test")
    print("=" * 60)
    
    # Test 1: Full PDF workflow
    await test_pdf_summary_workflow()
    
    # Test 2: Simple text summarization
    # await test_simple_summary()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main()) 