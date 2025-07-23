#!/usr/bin/env python3
"""
Test suite for the Intelligent Multi-Agent Orchestrator
Tests workflow composition, pattern matching, and execution
"""

import asyncio
import json
import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

# Add the src directory to the path
src_dir = str(Path(__file__).parent.parent.parent / "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from redaptive.orchestration import OrchestrationEngine
from redaptive.orchestration.planners import DynamicPlanner
from redaptive.orchestration.matchers import KeywordMatcher

class TestIntelligentOrchestrator:
    """Test the intelligent orchestrator functionality"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create a test orchestrator instance"""
        return IntelligentOrchestrator()
    
    @pytest.fixture
    def mock_agent_responses(self):
        """Mock responses from agents"""
        return {
            "textract": {
                "extract_text": {
                    "result": {
                        "content": [{
                            "text": json.dumps({
                                "full_text": "This is a sample document text for testing purposes.",
                                "total_blocks": 5
                            })
                        }]
                    }
                },
                "extract_tables": {
                    "result": {
                        "content": [{
                            "text": json.dumps({
                                "tables": [{"headers": ["Name", "Age"], "rows": [["John", "30"]]}]
                            })
                        }]
                    }
                }
            },
            "summarize": {
                "summarize_text": {
                    "result": {
                        "content": [{
                            "text": json.dumps({
                                "summary": "Sample document summary.",
                                "summary_length": 25
                            })
                        }]
                    }
                },
                "analyze_sentiment": {
                    "result": {
                        "content": [{
                            "text": json.dumps({
                                "sentiment": "positive",
                                "confidence": 0.85
                            })
                        }]
                    }
                }
            },
            "energy": {
                "analyze_consumption": {
                    "result": {
                        "content": [{
                            "text": json.dumps({
                                "analysis_id": "ENERGY123",
                                "consumption": 1250.5,
                                "efficiency_score": 85,
                                "recommendations": ["Install LED lighting", "Optimize HVAC schedule"]
                            })
                        }]
                    }
                },
                "get_usage_data": {
                    "result": {
                        "content": [{
                            "text": json.dumps({
                                "period": "2024-01",
                                "total_kwh": 1250.5,
                                "cost": 187.58,
                                "peak_demand": 15.2
                            })
                        }]
                    }
                }
            },
            "time": {
                "get_current_time": {
                    "result": {
                        "content": [{
                            "text": json.dumps({
                                "date": "2024-01-15",
                                "timezone": "America/Denver"
                            })
                        }]
                    }
                }
            }
        }
    
    def test_workflow_patterns_loaded(self, orchestrator):
        """Test that workflow patterns are properly loaded"""
        assert len(orchestrator.workflow_patterns) > 0
        
        # Check for key patterns
        expected_patterns = ["summarize_pdf", "analyze_document", "energy_data_analysis"]
        for pattern in expected_patterns:
            assert pattern in orchestrator.workflow_patterns
    
    def test_keyword_extraction(self, orchestrator):
        """Test keyword extraction from user requests"""
        test_cases = [
            ("summarize this PDF", ["document", "summarize"]),
            ("analyze the sentiment of this document", ["document", "analyze", "sentiment"]),
            ("extract tables from PDF", ["document", "extract"]),
            ("analyze energy consumption data", ["analyze", "energy", "consumption", "data"])
        ]
        
        for request, expected_keywords in test_cases:
            keywords = orchestrator._extract_keywords(request)
            for expected in expected_keywords:
                assert expected in keywords, f"Expected '{expected}' in keywords for '{request}'"
    
    def test_pattern_matching(self, orchestrator):
        """Test pattern matching against user requests"""
        test_cases = [
            ("summarize this PDF", "summarize_pdf"),
            ("give me a summary of this document", "summarize_pdf"),
            ("analyze the sentiment of this PDF", "analyze_document"),
            ("extract tables from this document", "extract_tables"),
            ("analyze energy consumption for this building", "energy_data_analysis"),
        ]
        
        for request, expected_pattern in test_cases:
            workflow_steps = orchestrator.plan_workflow(request, {"file_path": "test.pdf"})
            assert len(workflow_steps) > 0, f"No workflow planned for '{request}'"
            
            # Check that the workflow uses the expected agents
            pattern = orchestrator.workflow_patterns[expected_pattern]
            expected_agents = [step["agent"] for step in pattern["steps"]]
            actual_agents = [step.agent_name for step in workflow_steps]
            
            # Check that at least one expected agent is in the workflow
            found_agent = False
            for agent in expected_agents:
                if agent in actual_agents:
                    found_agent = True
                    break
            assert found_agent, f"Expected at least one agent from {expected_agents} in workflow for '{request}', got {actual_agents}"
    
    def test_intelligent_composition(self, orchestrator):
        """Test intelligent workflow composition for unknown requests"""
        # Test a request that doesn't match any pattern
        request = "process this document and give me insights"
        workflow_steps = orchestrator.plan_workflow(request, {"file_path": "test.pdf"})
        
        # Should still create a workflow using intelligent composition
        assert len(workflow_steps) > 0, "Intelligent composition should create a workflow"
    
    @pytest.mark.asyncio
    async def test_execute_intelligent_workflow(self, orchestrator, mock_agent_responses):
        """Test the complete intelligent workflow execution"""
        with patch.object(orchestrator, 'start_agents', new_callable=AsyncMock) as mock_start, \
             patch.object(orchestrator, 'stop_all_agents', new_callable=AsyncMock) as mock_stop, \
             patch.object(orchestrator, 'call_agent_tool', new_callable=AsyncMock) as mock_call:
            
            # Mock the agent tool calls
            async def mock_call_tool(agent_name, tool_name, arguments):
                return mock_agent_responses[agent_name][tool_name]
            
            mock_call.side_effect = mock_call_tool
            
            # Test PDF summarization
            result = await orchestrator.execute_intelligent_workflow(
                "summarize this PDF",
                {"file_path": "test.pdf", "max_length": 200}
            )
            
            # Verify the result
            assert "error" not in result
            assert result["workflow"] == "intelligent_workflow"
            assert result["user_goal"] == "summarize this PDF"
            assert result["steps_executed"] > 0
            
            # Verify agents were started and stopped
            mock_start.assert_called()
            mock_stop.assert_called()
    
    def test_argument_resolution(self, orchestrator):
        """Test argument resolution with step references"""
        # Mock results from previous steps
        results = {
            "step_0": {
                "result": {
                    "content": [{
                        "text": json.dumps({
                            "full_text": "Sample text from previous step"
                        })
                    }]
                }
            }
        }
        
        # Test arguments with placeholders
        arguments = {
            "text": "{{step_0.full_text}}",
            "max_length": 150
        }
        
        resolved = orchestrator._resolve_arguments(arguments, results)
        
        assert resolved["text"] == "Sample text from previous step"
        assert resolved["max_length"] == 150
    
    def test_workflow_summary_generation(self, orchestrator):
        """Test workflow summary generation"""
        workflow_steps = [
            WorkflowStep("textract", "extract_text", {"file_path": "test.pdf"}),
            WorkflowStep("summarize", "summarize_text", {"text": "{{step_0.full_text}}"})
        ]
        
        results = {
            "step_0": {
                "result": {
                    "content": [{
                        "text": json.dumps({
                            "full_text": "Sample text",
                            "total_blocks": 3
                        })
                    }]
                }
            },
            "step_1": {
                "result": {
                    "content": [{
                        "text": json.dumps({
                            "summary": "Sample summary",
                            "summary_length": 15
                        })
                    }]
                }
            }
        }
        
        summary = orchestrator._generate_workflow_summary(workflow_steps, results)
        assert "Executed workflow with 2 steps:" in summary
        assert "Generated 2 results" in summary

class TestProcessUserRequest:
    """Test the main process_user_request function"""
    
    @pytest.mark.asyncio
    async def test_pdf_summarization_request(self):
        """Test processing a PDF summarization request"""
        with patch('orchestration.intelligent.intelligent_orchestrator.IntelligentOrchestrator') as MockOrchestrator:
            mock_orchestrator = MockOrchestrator.return_value
            
            # Mock the execute_intelligent_workflow method
            mock_orchestrator.execute_intelligent_workflow = AsyncMock(return_value={
                "workflow": "intelligent_workflow",
                "user_goal": "summarize this PDF",
                "steps_executed": 2,
                "summary": "Extracted 50 characters; Generated 25 character summary"
            })
            
            result = await process_user_request(
                "summarize this PDF",
                file_path="test.pdf",
                max_length=200
            )
            
            # Verify the orchestrator was called correctly
            mock_orchestrator.execute_intelligent_workflow.assert_called_once_with(
                "summarize this PDF",
                {"file_path": "test.pdf", "max_length": 200}
            )
            
            # Verify the result
            assert result["workflow"] == "intelligent_workflow"
            assert result["user_goal"] == "summarize this PDF"
    
    @pytest.mark.asyncio
    async def test_sentiment_analysis_request(self):
        """Test processing a sentiment analysis request"""
        with patch('orchestration.intelligent.intelligent_orchestrator.IntelligentOrchestrator') as MockOrchestrator:
            mock_orchestrator = MockOrchestrator.return_value
            
            mock_orchestrator.execute_intelligent_workflow = AsyncMock(return_value={
                "workflow": "intelligent_workflow",
                "user_goal": "analyze the sentiment of this document",
                "steps_executed": 2,
                "summary": "Extracted 50 characters; Sentiment analysis completed"
            })
            
            result = await process_user_request(
                "analyze the sentiment of this document",
                file_path="test.pdf"
            )
            
            mock_orchestrator.execute_intelligent_workflow.assert_called_once_with(
                "analyze the sentiment of this document",
                {"file_path": "test.pdf"}
            )
            
            assert result["workflow"] == "intelligent_workflow"
    
    @pytest.mark.asyncio
    async def test_energy_analysis_request(self):
        """Test processing an energy analysis request"""
        with patch('orchestration.intelligent.intelligent_orchestrator.IntelligentOrchestrator') as MockOrchestrator:
            mock_orchestrator = MockOrchestrator.return_value
            
            mock_orchestrator.execute_intelligent_workflow = AsyncMock(return_value={
                "workflow": "intelligent_workflow",
                "user_goal": "analyze energy consumption for this building",
                "steps_executed": 2,
                "summary": "Energy analysis completed"
            })
            
            result = await process_user_request(
                "analyze energy consumption for this building",
                building_id=123,
                start_date="2024-01-01",
                end_date="2024-01-31",
                analysis_type="consumption"
            )
            
            expected_context = {
                "building_id": 123,
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "analysis_type": "consumption"
            }
            
            mock_orchestrator.execute_intelligent_workflow.assert_called_once_with(
                "analyze energy consumption for this building",
                expected_context
            )
            
            assert result["workflow"] == "intelligent_workflow"

class TestWorkflowPatterns:
    """Test specific workflow patterns"""
    
    def test_summarize_pdf_pattern(self):
        """Test the PDF summarization pattern"""
        orchestrator = IntelligentOrchestrator()
        pattern = orchestrator.workflow_patterns["summarize_pdf"]
        
        assert pattern["goal"] == "summarize PDF content"
        assert "pdf" in pattern["keywords"]
        assert "summarize" in pattern["keywords"]
        
        steps = pattern["steps"]
        assert len(steps) == 2
        assert steps[0]["agent"] == "textract"
        assert steps[0]["tool"] == "extract_text"
        assert steps[1]["agent"] == "summarize"
        assert steps[1]["tool"] == "summarize_text"
    
    def test_analyze_document_pattern(self):
        """Test the document analysis pattern"""
        orchestrator = IntelligentOrchestrator()
        pattern = orchestrator.workflow_patterns["analyze_document"]
        
        assert pattern["goal"] == "analyze document content and sentiment"
        assert "analyze" in pattern["keywords"]
        assert "sentiment" in pattern["keywords"]
        
        steps = pattern["steps"]
        assert len(steps) == 2
        assert steps[0]["agent"] == "textract"
        assert steps[0]["tool"] =="extract_text"
        assert steps[1]["agent"] == "summarize"
        assert steps[1]["tool"] == "analyze_sentiment"
    
    def test_energy_analysis_pattern(self):
        """Test the energy analysis pattern"""
        orchestrator = IntelligentOrchestrator()
        pattern = orchestrator.workflow_patterns["energy_data_analysis"]
        
        assert pattern["description"] == "Analyze energy data"
        assert "energy" in pattern["keywords"]
        assert "analyze" in pattern["keywords"]
        
        tools = pattern["tools"]
        assert len(tools) == 1
        assert "energy.analyze_consumption" in tools

class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_no_workflow_found(self):
        """Test handling when no suitable workflow is found"""
        with patch('orchestration.intelligent.intelligent_orchestrator.IntelligentOrchestrator') as MockOrchestrator:
            mock_orchestrator = MockOrchestrator.return_value
            
            # Mock no workflow found
            mock_orchestrator.execute_intelligent_workflow = AsyncMock(return_value={
                "error": "No suitable workflow found for: invalid request"
            })
            
            result = await process_user_request("invalid request")
            
            assert "error" in result
            assert "No suitable workflow found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_agent_failure(self):
        """Test handling when an agent fails"""
        with patch('orchestration.intelligent.intelligent_orchestrator.IntelligentOrchestrator') as MockOrchestrator:
            mock_orchestrator = MockOrchestrator.return_value
            
            # Mock agent failure
            mock_orchestrator.execute_intelligent_workflow = AsyncMock(return_value={
                "error": "Step step_0 failed: Agent textract not available"
            })
            
            result = await process_user_request("summarize this PDF", file_path="test.pdf")
            
            assert "error" in result
            assert "failed" in result["error"]

# Integration test that runs the actual examples
class TestIntegrationExamples:
    """Integration tests that run the actual examples"""
    
    @pytest.mark.asyncio
    async def test_example_workflows(self):
        """Test running the example workflows"""
        # This test would run the actual examples if agents were available
        # For now, we'll test the pattern matching and workflow planning
        
        orchestrator = IntelligentOrchestrator()
        
        # Test various example requests
        example_requests = [
            ("summarize this PDF", {"file_path": "test.pdf"}),
            ("analyze the sentiment of this document", {"file_path": "test.pdf"}),
            ("extract tables from this PDF", {"file_path": "test.pdf"}),
            ("analyze energy consumption for this building", {
                "building_id": 123,
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "analysis_type": "consumption"
            }),
            ("give me a complete analysis of this document", {
                "file_path": "test.pdf",
                "max_length": 300
            })
        ]
        
        for request, context in example_requests:
            # Test workflow planning
            workflow_steps = orchestrator.plan_workflow(request, context)
            assert len(workflow_steps) > 0, f"No workflow planned for: {request}"
            
            # Test that the workflow uses appropriate agents
            agent_names = [step.agent_name for step in workflow_steps]
            assert len(agent_names) > 0, f"No agents in workflow for: {request}"
            
            print(f"✅ {request} -> {len(workflow_steps)} steps using agents: {agent_names}")

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"]) 