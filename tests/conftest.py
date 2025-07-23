"""
Pytest configuration for Redaptive Agentic Platform tests.
"""

import sys
from pathlib import Path

# Add src to Python path for all tests
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import pytest
import asyncio
import logging

# Configure logging for tests
logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_database():
    """Mock database fixture for testing without real database."""
    class MockDB:
        def connect(self):
            return self
        
        def get_cursor(self):
            return self
        
        def __enter__(self):
            return self
        
        def __exit__(self, *args):
            pass
        
        def execute(self, query, params=None):
            pass
        
        def fetchall(self):
            return []
        
        def fetchone(self):
            return None
    
    return MockDB()

@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing."""
    return {
        "portfolio_id": "test_portfolio_001",
        "date_range": {
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        },
        "buildings": [
            {
                "building_id": "building_001",
                "building_name": "Test Office Building",
                "building_type": "office",
                "floor_area": 50000,
                "location": "San Francisco, CA"
            }
        ]
    }