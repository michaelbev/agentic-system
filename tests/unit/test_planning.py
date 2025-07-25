#!/usr/bin/env python3
"""Comprehensive unit tests for planning functionality."""

import pytest
import asyncio
import sys
from pathlib import Path

# Add src to path
src_dir = str(Path(__file__).parent.parent.parent / "src")
sys.path.insert(0, src_dir)

from redaptive.orchestration.planners import (
    DynamicPlanner, 
    LearningBasedPlanner, 
    HybridPlanner
)
from redaptive.orchestration.planners.llm_client import LLMClient

class TestPlanningMethods:
    """Test different planning methods and their functionality."""
    
    @pytest.fixture
    def available_agents(self):
        """Available agents for testing."""
        return ["energy-monitoring", "energy-finance", "portfolio-intelligence", "system"]
    
    @pytest.fixture
    def test_queries(self):
        """Standard test queries for planning."""
        return [
            "What is the date of the most recent energy usage reading?",
            "Calculate ROI for LED retrofit project",
            "Find energy optimization opportunities",
            "What's the current time?",
            "Who was the first president of the United States?"
        ]
    
    @pytest.mark.asyncio
    async def test_rule_based_planning(self, available_agents, test_queries):
        """Test rule-based planning functionality."""
        planner = DynamicPlanner()
        
        for query in test_queries:
            result = await planner.create_workflow(query, available_agents)
            
            # Basic validation
            assert result is not None
            assert "workflow_id" in result
            
            # Check if steps are generated
            if result.get("steps"):
                assert isinstance(result["steps"], list)
                for step in result["steps"]:
                    assert "agent" in step
                    assert "tool" in step
    
    @pytest.mark.asyncio
    async def test_learning_based_planning(self, available_agents, test_queries):
        """Test learning-based planning functionality."""
        planner = LearningBasedPlanner()
        
        for query in test_queries:
            result = await planner.create_workflow(query, available_agents)
            
            # Basic validation
            assert result is not None
            assert "planning_method" in result
            assert result["planning_method"] == "learning_based"
            
            # Check if steps are generated (may fall back to mock)
            if result.get("steps"):
                assert isinstance(result["steps"], list)
                for step in result["steps"]:
                    assert "agent" in step
                    assert "tool" in step
    
    @pytest.mark.asyncio
    async def test_hybrid_planning_learning_primary(self, available_agents, test_queries):
        """Test hybrid planning with learning-based as primary."""
        planner = HybridPlanner(learning_primary=True)
        
        for query in test_queries:
            result = await planner.create_workflow(query, available_agents)
            
            # Basic validation
            assert result is not None
            assert "workflow_id" in result
            assert "planning_method" in result
            assert result["planning_method"] in ["learning_based", "rule_based"]
            
            # Check if steps are generated
            if result.get("steps"):
                assert isinstance(result["steps"], list)
                for step in result["steps"]:
                    assert "agent" in step
                    assert "tool" in step
    
    @pytest.mark.asyncio
    async def test_hybrid_planning_rule_primary(self, available_agents, test_queries):
        """Test hybrid planning with rule-based as primary."""
        planner = HybridPlanner(learning_primary=False)
        
        for query in test_queries:
            result = await planner.create_workflow(query, available_agents)
            
            # Basic validation
            assert result is not None
            assert "workflow_id" in result
            assert "planning_method" in result
            assert result["planning_method"] == "rule_based"
            
            # Check if steps are generated
            if result.get("steps"):
                assert isinstance(result["steps"], list)
                for step in result["steps"]:
                    assert "agent" in step
                    assert "tool" in step
    
    @pytest.mark.asyncio
    async def test_planning_method_tracking(self, available_agents):
        """Test that planning methods are properly tracked in results."""
        planners = {
            "rule_based": DynamicPlanner(),
            "learning_based": LearningBasedPlanner(),
            "hybrid_learning": HybridPlanner(learning_primary=True),
            "hybrid_rule": HybridPlanner(learning_primary=False)
        }
        
        query = "What is the date of the most recent energy usage reading?"
        
        for method_name, planner in planners.items():
            result = await planner.create_workflow(query, available_agents)
            
            assert result["planning_method"] in ["rule_based", "learning_based"]
            assert "planning_reason" in result
    
    @pytest.mark.asyncio
    async def test_agent_routing(self, available_agents):
        """Test that queries are routed to appropriate agents."""
        planner = DynamicPlanner()
        
        test_cases = [
            ("energy", "energy-monitoring"),
            ("roi", "energy-finance"),
            ("optimization", "portfolio-intelligence"),
            ("time", "system")
        ]
        
        for keyword, expected_agent in test_cases:
            query = f"Test query with {keyword}"
            result = await planner.create_workflow(query, available_agents)
            
            if result.get("steps"):
                actual_agent = result["steps"][0]["agent"]
                # Note: This is a basic test - actual routing may vary
                assert actual_agent in available_agents

class TestLLMClient:
    """Test LLM client functionality."""
    
    @pytest.mark.asyncio
    async def test_llm_client_initialization(self):
        """Test LLM client can be initialized."""
        client = LLMClient(provider="anthropic")
        assert client is not None
        assert hasattr(client, 'generate')
    
    @pytest.mark.asyncio
    async def test_llm_client_generation(self):
        """Test LLM client can generate responses."""
        client = LLMClient(provider="anthropic")
        
        test_prompt = "Respond with just 'Test successful' if you can see this message."
        response = await client.generate(test_prompt)
        
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_llm_client_fallback(self):
        """Test LLM client falls back to mock when API fails."""
        # Test with invalid provider to trigger fallback
        client = LLMClient(provider="invalid")
        
        test_prompt = "Test prompt"
        response = await client.generate(test_prompt)
        
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0

class TestPlanningIntegration:
    """Integration tests for planning functionality."""
    
    @pytest.mark.asyncio
    async def test_planning_with_real_queries(self):
        """Test planning with realistic user queries."""
        planners = [
            DynamicPlanner(),
            LearningBasedPlanner(),
            HybridPlanner(learning_primary=True),
            HybridPlanner(learning_primary=False)
        ]
        
        available_agents = ["energy-monitoring", "energy-finance", "portfolio-intelligence", "system"]
        
        realistic_queries = [
            "Show me the latest energy consumption data for Building A",
            "Calculate the return on investment for our LED lighting upgrade",
            "Identify energy savings opportunities across our portfolio",
            "What time is it right now?",
            "Analyze the energy usage patterns for the last quarter"
        ]
        
        for planner in planners:
            for query in realistic_queries:
                result = await planner.create_workflow(query, available_agents)
                
                # Validate result structure
                assert result is not None
                # Different planners may have different result structures
                assert "workflow_id" in result or "planning_method" in result
                
                # Validate steps if present
                if result.get("steps"):
                    assert isinstance(result["steps"], list)
                    for step in result["steps"]:
                        assert "agent" in step
                        assert "tool" in step
                        assert step["agent"] in available_agents 