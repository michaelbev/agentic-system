"""
Integration tests for the Redaptive platform.
"""

import pytest
from unittest.mock import Mock, patch

from redaptive.config import settings
from redaptive.agents import AGENT_REGISTRY
from redaptive.orchestration import OrchestrationEngine
from redaptive.tools import DatabaseTool


class TestPlatformIntegration:
    """Test integration between platform components."""
    
    def test_platform_components_load(self):
        """Test that all platform components can be loaded."""
        # Test configuration loads
        assert settings.database.name == "energy_db"
        
        # Test agents are registered
        assert len(AGENT_REGISTRY) > 0
        assert 'portfolio-intelligence' in AGENT_REGISTRY
        
        # Test orchestration engine can be created
        engine = OrchestrationEngine()
        assert engine is not None
        
        # Test tools can be imported
        assert DatabaseTool is not None
    
    @patch('redaptive.agents.energy.portfolio_intelligence.db')
    def test_agent_creation_with_config(self, mock_db):
        """Test that agents can be created using configuration."""
        mock_db.connect.return_value = Mock()
        
        from redaptive.agents.energy import PortfolioIntelligenceAgent
        
        # Test agent uses configuration
        agent = PortfolioIntelligenceAgent()
        assert agent.name == "portfolio-intelligence-agent"
        
        # Test database connection was attempted
        mock_db.connect.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_orchestration_with_agents(self):
        """Test orchestration engine with agents."""
        engine = OrchestrationEngine()
        
        # Mock agents to avoid database connections
        mock_agent = Mock()
        mock_agent.tools = {
            'test_tool': Mock(
                name='test_tool',
                description='Test tool',
                handler=Mock(return_value={'result': 'success'})
            )
        }
        engine.agents['test-agent'] = mock_agent
        
        # Test workflow execution
        workflow = {
            'steps': [
                {
                    'agent': 'test-agent',
                    'tool': 'test_tool',
                    'parameters': {}
                }
            ]
        }
        
        result = await engine.execute_workflow('test_workflow', workflow)
        
        assert result['status'] == 'completed'
        assert 'results' in result
        assert 'step_1' in result['results']
    
    @patch('redaptive.tools.database.db')
    def test_tools_with_config(self, mock_db):
        """Test tools work with configuration."""
        mock_db.health_check.return_value = True
        
        result = DatabaseTool.health_check()
        
        assert result['status'] == 'healthy'
        assert result['database'] == 'energy_db'
        mock_db.health_check.assert_called_once()
    
    def test_environment_integration(self):
        """Test platform works with environment variables."""
        # Test that settings can be loaded from environment
        # (This is tested in unit tests, but here we test the integration)
        
        assert hasattr(settings, 'database')
        assert hasattr(settings, 'agents')
        assert hasattr(settings, 'orchestration')
        
        # Test that settings are used by components
        assert settings.agents.max_concurrent_agents >= 1
        assert settings.orchestration.max_workflow_depth >= 1