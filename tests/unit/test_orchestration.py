"""
Test orchestration functionality.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from redaptive.orchestration import OrchestrationEngine
from redaptive.orchestration.planners import DynamicPlanner
from redaptive.orchestration.matchers import KeywordMatcher


class TestOrchestrationEngine:
    """Test the orchestration engine."""
    
    def test_orchestration_engine_creation(self):
        """Test creating orchestration engine."""
        engine = OrchestrationEngine()
        assert engine.agents == {}
        assert engine.running_workflows == {}
        assert engine.max_concurrent > 0
    
    @pytest.mark.asyncio
    async def test_initialize_agents(self):
        """Test initializing agents."""
        engine = OrchestrationEngine()
        
        with patch('redaptive.orchestration.engine.get_agent') as mock_get_agent:
            mock_agent_class = Mock()
            mock_get_agent.return_value = mock_agent_class
            
            result = await engine.initialize_agents(['portfolio-intelligence'])
            
            assert result == True
            assert 'portfolio-intelligence' in engine.agents
            mock_agent_class.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_list_available_agents(self):
        """Test listing available agents."""
        engine = OrchestrationEngine()
        
        # Mock an agent
        mock_agent = Mock()
        mock_agent.tools = {
            'test_tool': Mock(name='test_tool', description='Test tool')
        }
        engine.agents['test-agent'] = mock_agent
        
        agents = await engine.list_available_agents()
        
        assert len(agents) == 1
        assert agents[0]['name'] == 'test-agent'
        assert agents[0]['status'] == 'initialized'
        assert len(agents[0]['tools']) == 1


class TestDynamicPlanner:
    """Test the dynamic planner."""
    
    @pytest.mark.asyncio
    async def test_create_workflow(self):
        """Test creating a workflow."""
        planner = DynamicPlanner()
        
        workflow = await planner.create_workflow(
            "analyze energy usage",
            ["portfolio-intelligence"]
        )
        
        assert isinstance(workflow, dict)
        assert 'workflow_id' in workflow
        assert 'steps' in workflow
        assert len(workflow['steps']) > 0


class TestKeywordMatcher:
    """Test the keyword matcher."""
    
    @pytest.mark.asyncio
    async def test_match_intent(self):
        """Test intent matching."""
        matcher = KeywordMatcher()
        
        # Test energy-related intent
        result = await matcher.match_intent("analyze energy consumption")
        
        assert isinstance(result, dict)
        assert 'intent' in result
        assert 'confidence' in result
        assert result['intent'] == 'energy'
        assert result['confidence'] > 0
        
        # Test portfolio-related intent
        result = await matcher.match_intent("show portfolio buildings")
        
        assert result['intent'] == 'portfolio'
        assert result['confidence'] > 0