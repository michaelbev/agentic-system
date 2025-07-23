"""
Test shared tools functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from redaptive.tools import DatabaseTool, DataProcessor


class TestDatabaseTool:
    """Test database tool functionality."""
    
    @patch('redaptive.tools.database.db')
    def test_health_check_healthy(self, mock_db):
        """Test database health check when healthy."""
        mock_db.health_check.return_value = True
        
        result = DatabaseTool.health_check()
        
        assert result['status'] == 'healthy'
        assert result['database'] == 'energy_db'
        assert 'timestamp' in result
    
    @patch('redaptive.tools.database.db')
    def test_health_check_unhealthy(self, mock_db):
        """Test database health check when unhealthy."""
        mock_db.health_check.return_value = False
        
        result = DatabaseTool.health_check()
        
        assert result['status'] == 'unhealthy'
        assert result['database'] == 'energy_db'
    
    @patch('redaptive.tools.database.db')
    def test_health_check_error(self, mock_db):
        """Test database health check with error."""
        mock_db.health_check.side_effect = Exception("Connection failed")
        
        result = DatabaseTool.health_check()
        
        assert result['status'] == 'error'
        assert 'error' in result
        assert result['error'] == 'Connection failed'


class TestDataProcessor:
    """Test data processor functionality."""
    
    def test_sanitize_financial_data(self):
        """Test sanitizing financial data."""
        from decimal import Decimal
        from datetime import datetime
        
        test_data = {
            'amount': Decimal('100.50'),
            'date': datetime(2024, 1, 1),
            'nested': {
                'cost': Decimal('50.25')
            },
            'list_data': [
                {'value': Decimal('25.75')},
                'string_value'
            ]
        }
        
        result = DataProcessor.sanitize_financial_data(test_data)
        
        assert result['amount'] == 100.50
        assert result['date'] == '2024-01-01T00:00:00'
        assert result['nested']['cost'] == 50.25
        assert result['list_data'][0]['value'] == 25.75
        assert result['list_data'][1] == 'string_value'
    
    def test_calculate_energy_metrics(self):
        """Test calculating energy metrics."""
        usage_data = [
            {'energy_consumption': 100, 'demand_kw': 50},
            {'energy_consumption': 150, 'demand_kw': 75},
            {'energy_consumption': 200, 'demand_kw': 100}
        ]
        
        result = DataProcessor.calculate_energy_metrics(usage_data)
        
        assert result['total_consumption'] == 450
        assert result['average_consumption'] == 150
        assert result['peak_demand'] == 100
        assert result['load_factor'] == 0.75  # 75/100
        assert 'efficiency_score' in result
    
    def test_calculate_energy_metrics_empty(self):
        """Test calculating metrics with empty data."""
        result = DataProcessor.calculate_energy_metrics([])
        
        assert result['total_consumption'] == 0.0
        assert result['average_consumption'] == 0.0
        assert result['peak_demand'] == 0.0
        assert result['load_factor'] == 0.0
        assert result['efficiency_score'] == 0.0
    
    def test_detect_anomalies(self):
        """Test anomaly detection."""
        # Normal values with one outlier
        values = [10, 12, 11, 13, 10, 11, 50, 12, 11]
        
        anomalies = DataProcessor.detect_anomalies(values, threshold=2.0)
        
        assert len(anomalies) == 1
        assert 6 in anomalies  # Index of the outlier value 50
    
    def test_detect_anomalies_no_anomalies(self):
        """Test anomaly detection with no anomalies."""
        values = [10, 12, 11, 13, 10, 11, 12, 11]
        
        anomalies = DataProcessor.detect_anomalies(values, threshold=2.0)
        
        assert len(anomalies) == 0
    
    def test_calculate_roi_metrics(self):
        """Test ROI calculation."""
        result = DataProcessor.calculate_roi_metrics(
            initial_cost=10000,
            annual_savings=2000,
            years=10
        )
        
        assert result['simple_payback'] == 5.0  # 10000/2000
        assert result['total_savings'] == 20000  # 2000*10
        assert result['roi_percentage'] == 100.0  # (20000-10000)/10000 * 100
        assert result['net_benefit'] == 10000  # 20000-10000
    
    def test_calculate_roi_metrics_invalid(self):
        """Test ROI calculation with invalid inputs."""
        result = DataProcessor.calculate_roi_metrics(
            initial_cost=0,
            annual_savings=2000,
            years=10
        )
        
        assert result['simple_payback'] == float('inf')
        assert result['roi_percentage'] == 0.0
        assert result['net_benefit'] == -0