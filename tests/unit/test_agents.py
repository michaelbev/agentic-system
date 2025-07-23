"""
Test agent functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from redaptive.agents import AGENT_REGISTRY, get_agent, list_agents


class TestAgentRegistry:
    """Test the agent registry functionality."""
    
    def test_agent_registry_exists(self):
        """Test that agent registry is populated."""
        assert isinstance(AGENT_REGISTRY, dict)
        assert len(AGENT_REGISTRY) > 0
        
        # Test expected agents are registered
        expected_agents = [
            'portfolio-intelligence',
            'energy-monitoring', 
            'energy-finance',
            'document-processing',
            'summarize'
        ]
        
        for agent_name in expected_agents:
            assert agent_name in AGENT_REGISTRY
    
    def test_get_agent(self):
        """Test getting agent by name."""
        # Test valid agent
        agent_class = get_agent('portfolio-intelligence')
        assert agent_class is not None
        
        # Test invalid agent
        invalid_agent = get_agent('non-existent-agent')
        assert invalid_agent is None
    
    def test_list_agents(self):
        """Test listing available agents."""
        agents = list_agents()
        assert isinstance(agents, list)
        assert len(agents) > 0
        assert 'portfolio-intelligence' in agents


class TestAgentBase:
    """Test base agent functionality."""
    
    @patch('redaptive.config.database.db')
    def test_portfolio_intelligence_agent_creation(self, mock_db):
        """Test creating portfolio intelligence agent."""
        mock_db.connect.return_value = Mock()
        
        from redaptive.agents.energy import PortfolioIntelligenceAgent
        
        agent = PortfolioIntelligenceAgent()
        assert agent.name == "portfolio-intelligence-agent"
        assert agent.version == "1.0.0"
        assert len(agent.tools) > 0
        
        # Test expected tools are registered
        expected_tools = [
            'analyze_portfolio_energy_usage',
            'identify_optimization_opportunities',
            'calculate_project_roi',
            'search_facilities',
            'book_service'
        ]
        
        for tool_name in expected_tools:
            assert tool_name in agent.tools
    
    @patch('redaptive.config.database.db')
    def test_energy_monitoring_agent_creation(self, mock_db):
        """Test creating energy monitoring agent."""
        mock_db.connect.return_value = Mock()
        
        from redaptive.agents.energy import EnergyMonitoringAgent
        
        agent = EnergyMonitoringAgent()
        assert agent.name == "energy-monitoring-agent"
        assert len(agent.tools) > 0
        
        # Test expected tools are registered
        expected_tools = [
            'process_meter_data',
            'detect_anomalies',
            'generate_field_alert'
        ]
        
        for tool_name in expected_tools:
            assert tool_name in agent.tools
    
    @patch('redaptive.config.database.db')
    def test_energy_finance_agent_creation(self, mock_db):
        """Test creating energy finance agent."""
        mock_db.connect.return_value = Mock()
        
        from redaptive.agents.energy import EnergyFinanceAgent
        
        agent = EnergyFinanceAgent()
        assert agent.name == "energy-finance-agent"
        assert len(agent.tools) > 0