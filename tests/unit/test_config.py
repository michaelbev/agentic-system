"""
Test configuration management.
"""

import pytest
import os
from unittest.mock import patch

from redaptive.config import settings
from redaptive.config.settings import DatabaseSettings, AgentSettings, OrchestrationSettings

class TestConfiguration:
    """Test configuration loading and management."""
    
    def test_default_settings(self):
        """Test default settings are loaded correctly."""
        # Host might be localhost or 127.0.0.1 depending on environment
        assert settings.database.host in ["localhost", "127.0.0.1"]
        assert settings.database.port == 5432
        assert settings.database.name == "energy_db"
        assert settings.agents.max_concurrent_agents == 10
        assert settings.orchestration.enable_intelligent_routing == True
    
    def test_database_settings_from_env(self):
        """Test database settings load from environment variables."""
        with patch.dict(os.environ, {
            'DB_HOST_ENERGY': 'test-host',
            'DB_PORT_ENERGY': '5433',
            'DB_NAME_ENERGY': 'test_db',
            'DB_USER_ENERGY': 'test_user',
            'DB_USERPASSWORD_ENERGY': 'test_pass'
        }):
            db_settings = DatabaseSettings.from_env()
            assert db_settings.host == 'test-host'
            assert db_settings.port == 5433
            assert db_settings.name == 'test_db'
            assert db_settings.user == 'test_user'
            assert db_settings.password == 'test_pass'
    
    def test_agent_settings_from_env(self):
        """Test agent settings load from environment variables."""
        with patch.dict(os.environ, {
            'MAX_CONCURRENT_AGENTS': '20',
            'AGENT_TIMEOUT': '60',
            'LOG_LEVEL': 'DEBUG'
        }):
            agent_settings = AgentSettings.from_env()
            assert agent_settings.max_concurrent_agents == 20
            assert agent_settings.default_timeout == 60
            assert agent_settings.log_level == 'DEBUG'
    
    def test_orchestration_settings_from_env(self):
        """Test orchestration settings load from environment variables."""
        with patch.dict(os.environ, {
            'ENABLE_INTELLIGENT_ROUTING': 'false',
            'MAX_WORKFLOW_DEPTH': '5',
            'CACHE_ENABLED': 'false'
        }):
            orch_settings = OrchestrationSettings.from_env()
            assert orch_settings.enable_intelligent_routing == False
            assert orch_settings.max_workflow_depth == 5
            assert orch_settings.cache_enabled == False