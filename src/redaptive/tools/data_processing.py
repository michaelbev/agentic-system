"""
Data processing utilities for the Redaptive platform.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from decimal import Decimal

logger = logging.getLogger(__name__)

class DataProcessor:
    """Utility class for common data processing operations."""
    
    @staticmethod
    def sanitize_financial_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize financial data for JSON serialization."""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, Decimal):
                sanitized[key] = float(value)
            elif isinstance(value, datetime):
                sanitized[key] = value.isoformat()
            elif isinstance(value, dict):
                sanitized[key] = DataProcessor.sanitize_financial_data(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    DataProcessor.sanitize_financial_data(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized
    
    @staticmethod
    def calculate_energy_metrics(usage_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate key energy performance metrics."""
        if not usage_data:
            return {
                "total_consumption": 0.0,
                "average_consumption": 0.0,
                "peak_demand": 0.0,
                "load_factor": 0.0,
                "efficiency_score": 0.0
            }
        
        consumptions = [float(row.get('energy_consumption', 0)) for row in usage_data]
        demands = [float(row.get('demand_kw', 0)) for row in usage_data if row.get('demand_kw')]
        
        total_consumption = sum(consumptions)
        avg_consumption = total_consumption / len(consumptions) if consumptions else 0
        peak_demand = max(demands) if demands else 0
        avg_demand = sum(demands) / len(demands) if demands else 0
        load_factor = avg_demand / peak_demand if peak_demand > 0 else 0
        
        # Simple efficiency score based on load factor and consumption variance
        consumption_variance = sum((x - avg_consumption) ** 2 for x in consumptions) / len(consumptions)
        efficiency_score = max(0, min(100, (load_factor * 50) + (50 - min(50, consumption_variance / avg_consumption * 10))))
        
        return {
            "total_consumption": total_consumption,
            "average_consumption": avg_consumption,
            "peak_demand": peak_demand,
            "load_factor": load_factor,
            "efficiency_score": efficiency_score
        }
    
    @staticmethod
    def aggregate_by_time_period(data: List[Dict[str, Any]], 
                               date_field: str = 'reading_date',
                               period: str = 'daily') -> Dict[str, List[Dict[str, Any]]]:
        """Aggregate data by time period (daily, weekly, monthly)."""
        aggregated = {}
        
        for record in data:
            try:
                if isinstance(record[date_field], str):
                    date = datetime.fromisoformat(record[date_field].replace('Z', '+00:00'))
                else:
                    date = record[date_field]
                
                if period == 'daily':
                    key = date.strftime('%Y-%m-%d')
                elif period == 'weekly':
                    # Week starting Monday
                    week_start = date - timedelta(days=date.weekday())
                    key = week_start.strftime('%Y-W%U')
                elif period == 'monthly':
                    key = date.strftime('%Y-%m')
                else:
                    key = date.strftime('%Y-%m-%d')
                
                if key not in aggregated:
                    aggregated[key] = []
                aggregated[key].append(record)
                
            except (ValueError, KeyError) as e:
                logger.warning(f"Skipping record with invalid date: {e}")
                continue
        
        return aggregated
    
    @staticmethod
    def detect_anomalies(values: List[float], threshold: float = 2.0) -> List[int]:
        """Detect anomalies using z-score method."""
        if len(values) < 3:
            return []
        
        mean_val = sum(values) / len(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return []
        
        anomalies = []
        for i, value in enumerate(values):
            z_score = abs((value - mean_val) / std_dev)
            if z_score > threshold:
                anomalies.append(i)
        
        return anomalies
    
    @staticmethod
    def format_currency(amount: Union[int, float, Decimal], currency: str = "USD") -> str:
        """Format currency values for display."""
        if isinstance(amount, Decimal):
            amount = float(amount)
        
        if currency == "USD":
            return f"${amount:,.2f}"
        else:
            return f"{amount:,.2f} {currency}"
    
    @staticmethod
    def calculate_roi_metrics(initial_cost: float, annual_savings: float, years: int = 10) -> Dict[str, float]:
        """Calculate comprehensive ROI metrics."""
        if initial_cost <= 0 or annual_savings <= 0:
            return {
                "simple_payback": float('inf'),
                "total_savings": 0.0,
                "roi_percentage": 0.0,
                "net_benefit": -initial_cost
            }
        
        simple_payback = initial_cost / annual_savings
        total_savings = annual_savings * years
        roi_percentage = ((total_savings - initial_cost) / initial_cost) * 100
        net_benefit = total_savings - initial_cost
        
        return {
            "simple_payback": simple_payback,
            "total_savings": total_savings,
            "roi_percentage": roi_percentage,
            "net_benefit": net_benefit
        }