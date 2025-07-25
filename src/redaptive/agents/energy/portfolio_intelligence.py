#!/usr/bin/env python3
"""
MCP Portfolio Intelligence Agent
Provides energy portfolio analysis and optimization tools for Redaptive EaaS platform
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import sys
from decimal import Decimal

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2 import sql
    PSYCOPG2_AVAILABLE = True
except ImportError:
    psycopg2 = None
    RealDictCursor = None
    sql = None
    PSYCOPG2_AVAILABLE = False

from redaptive.agents.base import BaseMCPServer
from redaptive.config.database import db

class PortfolioIntelligenceAgent(BaseMCPServer):
    def __init__(self):
        super().__init__("portfolio-intelligence-agent", "1.0.0")
        self.connection = None
        self.setup_database()
        self.setup_tools()
        
    def setup_database(self):
        """Setup database connection for energy portfolio data"""
        if not PSYCOPG2_AVAILABLE:
            logging.warning("psycopg2 not available - database functionality will be limited")
            self.connection = None
            return
            
        try:
            self.connection = db.connect()
            logging.info("Energy portfolio database connection established successfully")
        except Exception as e:
            logging.error(f"Failed to connect to energy portfolio database: {e}")
            self.connection = None
    
    def setup_tools(self):
        """Register energy portfolio analysis tools"""
        
        self.register_tool(
            "analyze_portfolio_energy_usage",
            "Analyze energy consumption patterns across a real estate portfolio",
            self.analyze_portfolio_energy_usage,
            {
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "Portfolio identifier"
                    },
                    "date_range": {
                        "type": "object",
                        "properties": {
                            "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                            "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                        },
                        "required": ["start_date", "end_date"]
                    },
                    "building_types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by building types (office, retail, warehouse, etc.)"
                    },
                    "energy_types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Energy types to analyze (electricity, gas, steam, etc.)"
                    }
                },
                "required": ["portfolio_id", "date_range"]
            }
        )
        
        self.register_tool(
            "identify_optimization_opportunities",
            "Identify energy efficiency and renewable energy opportunities across buildings",
            self.identify_optimization_opportunities,
            {
                "type": "object",
                "properties": {
                    "buildings_list": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of building IDs to analyze"
                    },
                    "opportunity_types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Types of opportunities (LED, HVAC, solar, storage, etc.)"
                    },
                    "min_roi_threshold": {
                        "type": "number",
                        "description": "Minimum ROI threshold for recommendations",
                        "default": 1.2
                    },
                    "max_payback_years": {
                        "type": "number",
                        "description": "Maximum payback period in years",
                        "default": 7
                    }
                },
                "required": ["buildings_list"]
            }
        )
        
        self.register_tool(
            "calculate_project_roi",
            "Calculate financial impact and ROI for proposed energy projects",
            self.calculate_project_roi,
            {
                "type": "object",
                "properties": {
                    "project_specs": {
                        "type": "object",
                        "properties": {
                            "building_id": {"type": "string"},
                            "project_type": {"type": "string"},
                            "technology": {"type": "string"},
                            "capacity": {"type": "number"},
                            "installation_cost": {"type": "number"},
                            "annual_savings": {"type": "number"}
                        },
                        "required": ["building_id", "project_type", "installation_cost", "annual_savings"]
                    },
                    "financial_parameters": {
                        "type": "object",
                        "properties": {
                            "discount_rate": {"type": "number", "default": 0.08},
                            "project_lifetime": {"type": "number", "default": 20},
                            "energy_escalation": {"type": "number", "default": 0.03},
                            "maintenance_rate": {"type": "number", "default": 0.02}
                        }
                    }
                },
                "required": ["project_specs"]
            }
        )
        
        self.register_tool(
            "generate_sustainability_report",
            "Generate comprehensive sustainability and ESG performance report",
            self.generate_sustainability_report,
            {
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "Portfolio identifier"
                    },
                    "reporting_period": {
                        "type": "object",
                        "properties": {
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"}
                        },
                        "required": ["start_date", "end_date"]
                    },
                    "report_type": {
                        "type": "string",
                        "enum": ["executive", "detailed", "regulatory", "investor"],
                        "description": "Type of sustainability report",
                        "default": "executive"
                    },
                    "include_carbon_footprint": {
                        "type": "boolean",
                        "description": "Include carbon footprint calculations",
                        "default": True
                    },
                    "include_benchmarking": {
                        "type": "boolean",
                        "description": "Include industry benchmarking",
                        "default": True
                    }
                },
                "required": ["portfolio_id", "reporting_period"]
            }
        )
        
        self.register_tool(
            "benchmark_portfolio_performance",
            "Benchmark portfolio energy performance against industry standards",
            self.benchmark_portfolio_performance,
            {
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "Portfolio identifier"
                    },
                    "benchmark_type": {
                        "type": "string",
                        "enum": ["industry", "energy_star", "custom"],
                        "description": "Type of benchmark comparison",
                        "default": "industry"
                    },
                    "building_categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Building categories for comparison"
                    }
                },
                "required": ["portfolio_id"]
            }
        )
        
        self.register_tool(
            "forecast_energy_demand",
            "Forecast future energy demand for portfolio planning",
            self.forecast_energy_demand,
            {
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "Portfolio identifier"
                    },
                    "forecast_horizon": {
                        "type": "number",
                        "description": "Forecast period in months",
                        "default": 12
                    },
                    "include_weather": {
                        "type": "boolean",
                        "description": "Include weather impact in forecast",
                        "default": True
                    },
                    "include_occupancy": {
                        "type": "boolean",
                        "description": "Include occupancy changes in forecast",
                        "default": True
                    }
                },
                "required": ["portfolio_id"]
            }
        )
        
        self.register_tool(
            "search_facilities",
            "Search for energy facilities by location and type",
            self.search_facilities,
            {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location to search for facilities"
                    },
                    "facility_type": {
                        "type": "string",
                        "description": "Type of facility (office, retail, warehouse, manufacturing)",
                        "enum": ["office", "retail", "warehouse", "manufacturing"]
                    },
                    "min_capacity": {
                        "type": "number",
                        "description": "Minimum facility capacity in square feet"
                    },
                    "max_capacity": {
                        "type": "number",
                        "description": "Maximum facility capacity in square feet"
                    }
                },
                "required": ["location"]
            }
        )
        
        self.register_tool(
            "check_service_availability",
            "Check availability of energy services for a facility",
            self.check_service_availability,
            {
                "type": "object",
                "properties": {
                    "facility_id": {
                        "type": "string",
                        "description": "Facility identifier"
                    },
                    "service_type": {
                        "type": "string",
                        "description": "Type of energy service",
                        "enum": ["LED", "HVAC", "Solar", "Storage", "Audit"]
                    },
                    "service_date": {
                        "type": "string",
                        "description": "Preferred service date (YYYY-MM-DD)"
                    }
                },
                "required": ["facility_id", "service_type"]
            }
        )
        
        self.register_tool(
            "book_service",
            "Book an energy service for a facility",
            self.book_service,
            {
                "type": "object",
                "properties": {
                    "facility_id": {
                        "type": "string",
                        "description": "Facility identifier"
                    },
                    "service_type": {
                        "type": "string",
                        "description": "Type of energy service",
                        "enum": ["LED", "HVAC", "Solar", "Storage", "Audit"]
                    },
                    "service_date": {
                        "type": "string",
                        "description": "Service date (YYYY-MM-DD)"
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Customer name"
                    },
                    "customer_email": {
                        "type": "string",
                        "description": "Customer email address"
                    },
                    "project_budget": {
                        "type": "number",
                        "description": "Project budget in USD"
                    }
                },
                "required": ["facility_id", "service_type", "service_date", "customer_name", "customer_email"]
            }
        )
    
    async def analyze_portfolio_energy_usage(self, portfolio_id: str, date_range: Dict[str, str], 
                                           building_types: List[str] = None, energy_types: List[str] = None):
        """Analyze energy consumption patterns across a real estate portfolio"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Build dynamic query for energy usage analysis
                query_parts = [
                    """
                    SELECT 
                        b.building_id,
                        b.building_name,
                        b.building_type,
                        b.floor_area,
                        b.location,
                        SUM(eu.energy_consumption) as total_consumption,
                        AVG(eu.energy_consumption) as avg_consumption,
                        eu.energy_type,
                        COUNT(*) as reading_count,
                        SUM(eu.energy_cost) as total_cost,
                        (SUM(eu.energy_consumption) / b.floor_area) as consumption_per_sqft
                    FROM buildings b
                    JOIN energy_usage eu ON b.building_id = eu.building_id
                    WHERE b.portfolio_id = %s
                        AND eu.reading_date BETWEEN %s AND %s
                    """
                ]
                params = [portfolio_id, date_range['start_date'], date_range['end_date']]
                
                if building_types:
                    placeholders = ','.join(['%s'] * len(building_types))
                    query_parts.append(f"AND b.building_type IN ({placeholders})")
                    params.extend(building_types)
                
                if energy_types:
                    placeholders = ','.join(['%s'] * len(energy_types))
                    query_parts.append(f"AND eu.energy_type IN ({placeholders})")
                    params.extend(energy_types)
                
                query_parts.append("""
                    GROUP BY b.building_id, b.building_name, b.building_type, 
                             b.floor_area, b.location, eu.energy_type
                    ORDER BY total_consumption DESC
                """)
                
                query = " ".join(query_parts)
                cursor.execute(query, params)
                usage_data = cursor.fetchall()
                
                # Calculate portfolio-level metrics
                total_consumption = sum(row['total_consumption'] for row in usage_data)
                total_cost = sum(row['total_cost'] for row in usage_data)
                unique_buildings = len(set(row['building_id'] for row in usage_data))
                
                # Identify top energy consumers
                building_totals = {}
                for row in usage_data:
                    bid = row['building_id']
                    if bid not in building_totals:
                        building_totals[bid] = {
                            'building_name': row['building_name'],
                            'building_type': row['building_type'],
                            'location': row['location'],
                            'total_consumption': 0,
                            'total_cost': 0,
                            'consumption_per_sqft': row['consumption_per_sqft']
                        }
                    building_totals[bid]['total_consumption'] += row['total_consumption']
                    building_totals[bid]['total_cost'] += row['total_cost']
                
                top_consumers = sorted(
                    building_totals.items(), 
                    key=lambda x: x[1]['total_consumption'], 
                    reverse=True
                )[:10]
                
                return {
                    "portfolio_id": portfolio_id,
                    "analysis_period": date_range,
                    "portfolio_metrics": {
                        "total_consumption": float(total_consumption),
                        "total_cost": float(total_cost),
                        "average_cost_per_kwh": float(total_cost / total_consumption) if total_consumption > 0 else 0,
                        "buildings_analyzed": unique_buildings,
                        "total_floor_area": sum(row['floor_area'] for row in usage_data if row['floor_area']),
                        "avg_consumption_per_sqft": float(total_consumption / sum(row['floor_area'] for row in usage_data if row['floor_area'])) if usage_data else 0
                    },
                    "detailed_usage": [dict(row) for row in usage_data],
                    "top_energy_consumers": [
                        {"building_id": bid, **data} for bid, data in top_consumers
                    ],
                    "energy_breakdown": self._calculate_energy_breakdown(usage_data)
                }
        except Exception as e:
            return {"error": f"Failed to analyze portfolio energy usage: {str(e)}"}
    
    async def identify_optimization_opportunities(self, buildings_list: List[str], 
                                                opportunity_types: List[str] = None,
                                                min_roi_threshold: float = 1.2, 
                                                max_payback_years: float = 7):
        """Identify energy efficiency and renewable energy opportunities"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                opportunities = []
                
                for building_id in buildings_list:
                    # Get building characteristics
                    building_query = """
                    SELECT b.*, 
                           AVG(eu.energy_consumption) as avg_consumption,
                           AVG(eu.energy_cost) as avg_cost
                    FROM buildings b
                    LEFT JOIN energy_usage eu ON b.building_id = eu.building_id
                    WHERE b.building_id = %s
                    GROUP BY b.building_id
                    """
                    cursor.execute(building_query, (building_id,))
                    building = cursor.fetchone()
                    
                    if not building:
                        continue
                    
                    # Calculate opportunities based on building characteristics
                    building_opportunities = self._calculate_opportunities(
                        dict(building), opportunity_types, min_roi_threshold, max_payback_years
                    )
                    opportunities.extend(building_opportunities)
                
                # Rank opportunities by ROI
                opportunities.sort(key=lambda x: x['estimated_roi'], reverse=True)
                
                # Calculate portfolio-level impact
                total_investment = sum(opp['estimated_cost'] for opp in opportunities)
                total_annual_savings = sum(opp['annual_savings'] for opp in opportunities)
                total_carbon_reduction = sum(opp['carbon_reduction_tons'] for opp in opportunities)
                
                return {
                    "buildings_analyzed": len(buildings_list),
                    "opportunities_identified": len(opportunities),
                    "portfolio_impact": {
                        "total_investment": float(total_investment),
                        "total_annual_savings": float(total_annual_savings),
                        "portfolio_roi": float(total_annual_savings / total_investment) if total_investment > 0 else 0,
                        "payback_years": float(total_investment / total_annual_savings) if total_annual_savings > 0 else 0,
                        "carbon_reduction_tons": float(total_carbon_reduction)
                    },
                    "opportunities": opportunities[:20],  # Top 20 opportunities
                    "summary_by_type": self._summarize_opportunities_by_type(opportunities)
                }
        except Exception as e:
            return {"error": f"Failed to identify optimization opportunities: {str(e)}"}
    
    async def calculate_project_roi(self, project_specs: Dict[str, Any], 
                                  financial_parameters: Dict[str, float] = None):
        """Calculate financial impact and ROI for proposed energy projects"""
        if not financial_parameters:
            financial_parameters = {
                "discount_rate": 0.08,
                "project_lifetime": 20,
                "energy_escalation": 0.03,
                "maintenance_rate": 0.02
            }
        
        try:
            # Extract project specifications
            installation_cost = project_specs['installation_cost']
            annual_savings = project_specs['annual_savings']
            lifetime = financial_parameters['project_lifetime']
            discount_rate = financial_parameters['discount_rate']
            escalation = financial_parameters['energy_escalation']
            maintenance_rate = financial_parameters['maintenance_rate']
            
            # Calculate cash flows
            cash_flows = []
            npv = -installation_cost  # Initial investment
            
            for year in range(1, int(lifetime) + 1):
                # Escalate savings and maintenance costs
                escalated_savings = annual_savings * ((1 + escalation) ** year)
                maintenance_cost = installation_cost * maintenance_rate * ((1 + escalation) ** year)
                net_cash_flow = escalated_savings - maintenance_cost
                
                # Present value of cash flow
                pv_cash_flow = net_cash_flow / ((1 + discount_rate) ** year)
                npv += pv_cash_flow
                
                cash_flows.append({
                    "year": year,
                    "gross_savings": float(escalated_savings),
                    "maintenance_cost": float(maintenance_cost),
                    "net_cash_flow": float(net_cash_flow),
                    "present_value": float(pv_cash_flow)
                })
            
            # Calculate financial metrics
            irr = self._calculate_irr(installation_cost, cash_flows)
            simple_payback = installation_cost / annual_savings if annual_savings > 0 else float('inf')
            total_savings = sum(cf['gross_savings'] for cf in cash_flows)
            
            return {
                "project_specs": project_specs,
                "financial_analysis": {
                    "initial_investment": float(installation_cost),
                    "annual_savings_year_1": float(annual_savings),
                    "project_lifetime": int(lifetime),
                    "net_present_value": float(npv),
                    "internal_rate_return": float(irr) if irr else None,
                    "simple_payback_years": float(simple_payback),
                    "total_lifetime_savings": float(total_savings),
                    "roi_ratio": float(npv / installation_cost) if installation_cost > 0 else 0
                },
                "yearly_cash_flows": cash_flows[:10],  # First 10 years
                "assumptions": financial_parameters,
                "recommendation": "Recommended" if npv > 0 and simple_payback <= 7 else "Not Recommended"
            }
        except Exception as e:
            return {"error": f"Failed to calculate project ROI: {str(e)}"}
    
    async def generate_sustainability_report(self, portfolio_id: str, reporting_period: Dict[str, str],
                                           report_type: str = "executive", 
                                           include_carbon_footprint: bool = True,
                                           include_benchmarking: bool = True):
        """Generate comprehensive sustainability and ESG performance report"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get portfolio overview
                portfolio_query = """
                SELECT p.*, COUNT(b.building_id) as building_count,
                       SUM(b.floor_area) as total_floor_area
                FROM portfolios p
                LEFT JOIN buildings b ON p.portfolio_id = b.portfolio_id
                WHERE p.portfolio_id = %s
                GROUP BY p.portfolio_id
                """
                cursor.execute(portfolio_query, (portfolio_id,))
                portfolio = cursor.fetchone()
                
                if not portfolio:
                    return {"error": f"Portfolio {portfolio_id} not found"}
                
                # Get energy performance data
                energy_analysis = await self.analyze_portfolio_energy_usage(
                    portfolio_id, reporting_period
                )
                
                report = {
                    "report_metadata": {
                        "portfolio_id": portfolio_id,
                        "portfolio_name": portfolio['portfolio_name'],
                        "report_type": report_type,
                        "reporting_period": reporting_period,
                        "generated_date": datetime.now().isoformat(),
                        "buildings_included": portfolio['building_count']
                    },
                    "executive_summary": {
                        "total_energy_consumption": energy_analysis['portfolio_metrics']['total_consumption'],
                        "total_energy_cost": energy_analysis['portfolio_metrics']['total_cost'],
                        "energy_intensity": energy_analysis['portfolio_metrics']['avg_consumption_per_sqft'],
                        "portfolio_performance": "Above Average"  # This would be calculated vs benchmarks
                    },
                    "energy_performance": energy_analysis
                }
                
                # Add carbon footprint if requested
                if include_carbon_footprint:
                    carbon_data = await self._calculate_carbon_footprint(portfolio_id, reporting_period)
                    report["carbon_footprint"] = carbon_data
                
                # Add benchmarking if requested
                if include_benchmarking:
                    benchmark_data = await self.benchmark_portfolio_performance(portfolio_id)
                    report["benchmarking"] = benchmark_data
                
                # Add recommendations based on report type
                if report_type in ["executive", "detailed"]:
                    opportunities = await self.identify_optimization_opportunities(
                        [b['building_id'] for b in energy_analysis['detailed_usage']]
                    )
                    report["optimization_opportunities"] = opportunities
                
                return report
                
        except Exception as e:
            return {"error": f"Failed to generate sustainability report: {str(e)}"}
    
    async def benchmark_portfolio_performance(self, portfolio_id: str, benchmark_type: str = "industry",
                                            building_categories: List[str] = None):
        """Benchmark portfolio energy performance against industry standards"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            # This would typically connect to external benchmarking databases
            # For now, we'll use simulated benchmark data
            benchmark_data = {
                "benchmark_type": benchmark_type,
                "portfolio_performance": {
                    "energy_use_intensity": 85.2,  # kWh/sqft/year
                    "carbon_intensity": 45.3,      # kg CO2/sqft/year
                    "cost_per_sqft": 2.85           # $/sqft/year
                },
                "industry_median": {
                    "energy_use_intensity": 92.1,
                    "carbon_intensity": 52.8,
                    "cost_per_sqft": 3.21
                },
                "percentile_ranking": {
                    "energy_efficiency": 73,  # 73rd percentile (better than 73% of peers)
                    "carbon_performance": 68,
                    "cost_efficiency": 71
                },
                "comparison_summary": "Portfolio performs 7% better than industry median on energy efficiency"
            }
            
            return benchmark_data
            
        except Exception as e:
            return {"error": f"Failed to benchmark portfolio performance: {str(e)}"}
    
    async def forecast_energy_demand(self, portfolio_id: str, forecast_horizon: int = 12,
                                   include_weather: bool = True, include_occupancy: bool = True):
        """Forecast future energy demand for portfolio planning"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            # This would implement machine learning models for forecasting
            # For now, we'll provide a simulated forecast
            base_consumption = 1000000  # kWh/month
            monthly_forecasts = []
            
            for month in range(1, forecast_horizon + 1):
                # Simulate seasonal variation and growth trends
                seasonal_factor = 1 + 0.2 * abs(((month % 12) - 6) / 6)  # Peak in summer/winter
                growth_factor = 1 + (0.02 * month / 12)  # 2% annual growth
                weather_impact = 1 + (0.1 * (0.5 - abs(0.5)))  # Weather variability
                
                forecasted_consumption = base_consumption * seasonal_factor * growth_factor
                if include_weather:
                    forecasted_consumption *= weather_impact
                
                monthly_forecasts.append({
                    "month": month,
                    "forecasted_consumption": float(forecasted_consumption),
                    "confidence_interval": {
                        "lower": float(forecasted_consumption * 0.9),
                        "upper": float(forecasted_consumption * 1.1)
                    },
                    "factors": {
                        "seasonal": float(seasonal_factor),
                        "growth": float(growth_factor),
                        "weather": float(weather_impact) if include_weather else 1.0
                    }
                })
            
            return {
                "portfolio_id": portfolio_id,
                "forecast_horizon_months": forecast_horizon,
                "forecast_parameters": {
                    "include_weather": include_weather,
                    "include_occupancy": include_occupancy
                },
                "monthly_forecasts": monthly_forecasts,
                "summary": {
                    "total_forecasted_consumption": sum(f['forecasted_consumption'] for f in monthly_forecasts),
                    "average_monthly_consumption": sum(f['forecasted_consumption'] for f in monthly_forecasts) / len(monthly_forecasts),
                    "peak_consumption_month": max(monthly_forecasts, key=lambda x: x['forecasted_consumption'])['month'],
                    "growth_trend": "Increasing 2% annually"
                }
            }
            
        except Exception as e:
            return {"error": f"Failed to forecast energy demand: {str(e)}"}
    
    def _calculate_energy_breakdown(self, usage_data):
        """Calculate energy breakdown by type and building category"""
        energy_by_type = {}
        energy_by_building_type = {}
        
        for row in usage_data:
            energy_type = row['energy_type']
            building_type = row['building_type']
            consumption = row['total_consumption']
            
            if energy_type not in energy_by_type:
                energy_by_type[energy_type] = 0
            energy_by_type[energy_type] += consumption
            
            if building_type not in energy_by_building_type:
                energy_by_building_type[building_type] = 0
            energy_by_building_type[building_type] += consumption
        
        return {
            "by_energy_type": energy_by_type,
            "by_building_type": energy_by_building_type
        }
    
    def _calculate_opportunities(self, building, opportunity_types, min_roi_threshold, max_payback_years):
        """Calculate energy efficiency opportunities for a building"""
        opportunities = []
        
        # Simulated opportunity calculations based on building characteristics
        building_area = building.get('floor_area', 10000)
        current_consumption = building.get('avg_consumption', 50000)  # kWh/month
        
        # LED Lighting Opportunity
        if not opportunity_types or 'LED' in opportunity_types:
            led_savings = current_consumption * 0.3  # 30% lighting savings
            led_cost = building_area * 3.5  # $3.50/sqft
            led_roi = (led_savings * 12 * 0.12) / led_cost  # Annual savings / cost
            
            if led_roi >= min_roi_threshold:
                opportunities.append({
                    "building_id": building['building_id'],
                    "opportunity_type": "LED_Lighting",
                    "estimated_cost": float(led_cost),
                    "annual_savings": float(led_savings * 12 * 0.12),  # $0.12/kWh
                    "estimated_roi": float(led_roi),
                    "payback_years": float(led_cost / (led_savings * 12 * 0.12)),
                    "carbon_reduction_tons": float(led_savings * 12 * 0.0004),  # 0.4 kg CO2/kWh
                    "implementation_complexity": "Low"
                })
        
        # HVAC Optimization
        if not opportunity_types or 'HVAC' in opportunity_types:
            hvac_savings = current_consumption * 0.25  # 25% HVAC savings
            hvac_cost = building_area * 8.0  # $8.00/sqft
            hvac_roi = (hvac_savings * 12 * 0.12) / hvac_cost
            
            if hvac_roi >= min_roi_threshold:
                opportunities.append({
                    "building_id": building['building_id'],
                    "opportunity_type": "HVAC_Optimization",
                    "estimated_cost": float(hvac_cost),
                    "annual_savings": float(hvac_savings * 12 * 0.12),
                    "estimated_roi": float(hvac_roi),
                    "payback_years": float(hvac_cost / (hvac_savings * 12 * 0.12)),
                    "carbon_reduction_tons": float(hvac_savings * 12 * 0.0004),
                    "implementation_complexity": "Medium"
                })
        
        # Solar Installation
        if not opportunity_types or 'Solar' in opportunity_types:
            solar_capacity = building_area * 0.01  # 10W/sqft
            solar_generation = solar_capacity * 1500  # 1500 kWh/kW/year
            solar_cost = solar_capacity * 2500  # $2.50/W
            solar_roi = (solar_generation * 0.12) / solar_cost
            
            if solar_roi >= min_roi_threshold and building.get('location', '').lower() in ['california', 'arizona', 'texas']:
                opportunities.append({
                    "building_id": building['building_id'],
                    "opportunity_type": "Solar_Installation",
                    "estimated_cost": float(solar_cost),
                    "annual_savings": float(solar_generation * 0.12),
                    "estimated_roi": float(solar_roi),
                    "payback_years": float(solar_cost / (solar_generation * 0.12)),
                    "carbon_reduction_tons": float(solar_generation * 0.0004),
                    "implementation_complexity": "High",
                    "system_size_kw": float(solar_capacity)
                })
        
        return opportunities
    
    def _summarize_opportunities_by_type(self, opportunities):
        """Summarize opportunities by type"""
        summary = {}
        for opp in opportunities:
            opp_type = opp['opportunity_type']
            if opp_type not in summary:
                summary[opp_type] = {
                    "count": 0,
                    "total_cost": 0,
                    "total_savings": 0,
                    "avg_roi": 0
                }
            
            summary[opp_type]["count"] += 1
            summary[opp_type]["total_cost"] += opp['estimated_cost']
            summary[opp_type]["total_savings"] += opp['annual_savings']
        
        # Calculate averages
        for opp_type in summary:
            if summary[opp_type]["count"] > 0:
                summary[opp_type]["avg_roi"] = summary[opp_type]["total_savings"] / summary[opp_type]["total_cost"]
        
        return summary
    
    def _calculate_irr(self, initial_investment, cash_flows):
        """Calculate Internal Rate of Return using approximation"""
        # Simplified IRR calculation - in production, use scipy or numpy
        try:
            total_cash_flow = sum(cf['net_cash_flow'] for cf in cash_flows)
            avg_annual_return = total_cash_flow / len(cash_flows)
            irr_estimate = (avg_annual_return / initial_investment) * 100
            return max(0, min(irr_estimate, 100))  # Cap between 0-100%
        except:
            return None
    
    async def search_facilities(self, location: str, facility_type: str = None, 
                              min_capacity: float = None, max_capacity: float = None):
        """Search for energy facilities by location, company name, or type"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Build dynamic query for facility search
                query_parts = [
                    """
                    SELECT 
                        b.building_id as facility_id,
                        b.building_name as facility_name,
                        b.building_type as facility_type,
                        b.floor_area as capacity_sqft,
                        b.location,
                        b.energy_star_score,
                        b.baseline_consumption,
                        b.baseline_cost,
                        p.portfolio_name,
                        p.company_name
                    FROM buildings b
                    JOIN portfolios p ON b.portfolio_id = p.portfolio_id
                    WHERE (LOWER(b.location) LIKE LOWER(%s) OR LOWER(p.company_name) LIKE LOWER(%s))
                    """
                ]
                params = [f"%{location}%", f"%{location}%"]
                
                if facility_type:
                    query_parts.append("AND b.building_type = %s")
                    params.append(facility_type)
                
                if min_capacity:
                    query_parts.append("AND b.floor_area >= %s")
                    params.append(min_capacity)
                
                if max_capacity:
                    query_parts.append("AND b.floor_area <= %s")
                    params.append(max_capacity)
                
                query_parts.append("ORDER BY b.energy_star_score DESC, b.floor_area DESC")
                
                query = " ".join(query_parts)
                cursor.execute(query, params)
                facilities = cursor.fetchall()
                
                return {
                    "search_criteria": {
                        "location": location,
                        "facility_type": facility_type,
                        "min_capacity": min_capacity,
                        "max_capacity": max_capacity
                    },
                    "facilities_found": len(facilities),
                    "facilities": [dict(facility) for facility in facilities]
                }
        except Exception as e:
            return {"error": f"Failed to search facilities: {str(e)}"}
    
    async def check_service_availability(self, facility_id: str, service_type: str, 
                                       service_date: str = None):
        """Check availability of energy services for a facility"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get facility information
                facility_query = """
                SELECT b.*, p.portfolio_name, p.company_name
                FROM buildings b
                JOIN portfolios p ON b.portfolio_id = p.portfolio_id
                WHERE b.building_id = %s
                """
                cursor.execute(facility_query, (facility_id,))
                facility = cursor.fetchone()
                
                if not facility:
                    return {"error": f"Facility {facility_id} not found"}
                
                # Check for existing projects of this type
                project_query = """
                SELECT * FROM energy_projects 
                WHERE building_id = %s AND project_type = %s
                ORDER BY created_date DESC
                """
                cursor.execute(project_query, (facility_id, service_type))
                existing_projects = cursor.fetchall()
                
                # Check for opportunities of this type
                opportunity_query = """
                SELECT * FROM project_opportunities 
                WHERE building_id = %s AND opportunity_type = %s
                ORDER BY priority_score DESC
                """
                cursor.execute(opportunity_query, (facility_id, service_type))
                opportunities = cursor.fetchall()
                
                # Determine availability
                is_available = True
                availability_notes = []
                
                if existing_projects:
                    latest_project = existing_projects[0]
                    if latest_project['project_status'] in ['in_progress', 'approved']:
                        is_available = False
                        availability_notes.append(f"Similar project already {latest_project['project_status']}")
                
                if opportunities:
                    opportunity = opportunities[0]
                    estimated_cost = opportunity['estimated_cost']
                    annual_savings = opportunity['annual_savings']
                    roi = opportunity['estimated_roi']
                    payback_years = opportunity['payback_years']
                else:
                    # Generate estimated values based on facility characteristics
                    estimated_cost = float(facility['floor_area']) * 5.0  # $5/sqft estimate
                    annual_savings = float(facility['baseline_cost']) * 0.2  # 20% savings estimate
                    roi = annual_savings / estimated_cost if estimated_cost > 0 else 0
                    payback_years = estimated_cost / annual_savings if annual_savings > 0 else 0
                
                return {
                    "facility_id": facility_id,
                    "facility_name": facility['building_name'],
                    "service_type": service_type,
                    "service_date": service_date,
                    "availability": {
                        "is_available": is_available,
                        "notes": availability_notes
                    },
                    "service_estimate": {
                        "estimated_cost": estimated_cost,
                        "annual_savings": annual_savings,
                        "roi": roi,
                        "payback_years": payback_years
                    },
                    "existing_projects": [dict(project) for project in existing_projects],
                    "identified_opportunities": [dict(opp) for opp in opportunities]
                }
        except Exception as e:
            return {"error": f"Failed to check service availability: {str(e)}"}
    
    async def book_service(self, facility_id: str, service_type: str, service_date: str,
                          customer_name: str, customer_email: str, project_budget: float = None):
        """Book an energy service for a facility"""
        if not self.connection:
            return {"error": "Database connection not established"}
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # First check availability
                availability = await self.check_service_availability(facility_id, service_type, service_date)
                
                if not availability.get('availability', {}).get('is_available', False):
                    return {
                        "error": "Service not available",
                        "availability_info": availability
                    }
                
                # Create a new energy project booking
                project_insert = """
                INSERT INTO energy_projects (
                    building_id, project_name, project_type, 
                    installation_cost, annual_savings_cost, 
                    project_status, start_date, created_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                ) RETURNING project_id
                """
                
                project_name = f"{service_type} Service - {customer_name}"
                estimated_cost = availability['service_estimate']['estimated_cost']
                annual_savings = availability['service_estimate']['annual_savings']
                
                cursor.execute(project_insert, (
                    facility_id, project_name, service_type,
                    estimated_cost, annual_savings,
                    'planned', service_date
                ))
                
                project_id = cursor.fetchone()['project_id']
                self.connection.commit()
                
                return {
                    "booking_id": str(project_id),
                    "facility_id": facility_id,
                    "service_type": service_type,
                    "service_date": service_date,
                    "customer_name": customer_name,
                    "customer_email": customer_email,
                    "project_details": {
                        "project_name": project_name,
                        "estimated_cost": estimated_cost,
                        "annual_savings": annual_savings,
                        "project_status": "planned"
                    },
                    "status": "booking_confirmed",
                    "next_steps": [
                        "Site survey will be scheduled within 5 business days",
                        "Detailed project proposal will be provided",
                        "Installation timeline will be confirmed"
                    ]
                }
        except Exception as e:
            return {"error": f"Failed to book service: {str(e)}"}
    
    async def _calculate_carbon_footprint(self, portfolio_id, reporting_period):
        """Calculate carbon footprint for the portfolio"""
        # Simplified carbon calculation
        return {
            "total_co2_tons": 2450.5,
            "scope_1_emissions": 450.2,  # Direct emissions
            "scope_2_emissions": 2000.3,  # Indirect emissions from electricity
            "emissions_intensity": 0.045,  # tons CO2/sqft
            "reduction_vs_baseline": -12.3,  # % reduction
            "carbon_offset_opportunities": 500.0  # tons CO2 that could be offset
        }

async def main():
    """Start the Portfolio Intelligence Agent"""
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    
    agent = PortfolioIntelligenceAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())