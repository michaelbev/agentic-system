"""Dynamic workflow planner."""

import re
from typing import Dict, List, Any
from .base_planner import BasePlanner

class DynamicPlanner(BasePlanner):
    """Dynamic planner that adapts workflows based on context."""
    
    async def create_workflow(self, user_request: str, 
                            available_agents: List[str]) -> Dict[str, Any]:
        """Create a workflow plan from user request."""
        
        # Validate available agents
        if not available_agents:
            return {"workflow_id": "no_agents_workflow", "steps": []}
        
        # Determine workflow type based on user request
        user_lower = user_request.lower()
        
        # Handle out-of-scope requests
        if any(word in user_lower for word in ["president", "history", "politics", "government", "election", "weather", "forecast", "sports", "football", "recipe", "cook", "capital", "country", "geography"]):
            return {
                "workflow_id": "out_of_scope_workflow",
                "steps": [
                    {
                        "agent": "system",
                        "tool": "scope_check",
                        "parameters": {
                            "scope": "out_of_bounds",
                            "system_domain": "Energy-as-a-Service (EaaS) portfolio management and optimization",
                            "supported_topics": ["energy consumption", "portfolio analysis", "financial optimization", "document processing", "time/date"],
                            "unsupported_topics": ["historical facts", "politics", "general knowledge", "weather", "sports", "cooking", "geography"],
                            "recommendation": "Please ask questions related to energy portfolio management, building optimization, financial analysis, or document processing."
                        }
                    }
                ]
            }
        
        # Handle time/date requests
        if any(word in user_lower for word in ["date", "time", "current", "now", "today", "what time", "what date"]):
            return {
                "workflow_id": "time_analysis_workflow",
                "steps": [
                    {
                        "agent": "system", 
                        "tool": "get_current_time",
                        "parameters": {
                            "timezone": "America/Denver"
                        }
                    }
                ]
            }
        
        # Handle energy analysis requests
        if any(word in user_lower for word in ["energy", "consumption", "usage"]):
            # Extract building number dynamically
            building_id = "building_123"  # Default
            building_match = re.search(r'building\s+(\d+)', user_lower)
            if building_match:
                building_id = f"building_{building_match.group(1)}"
            
            # Extract date range if mentioned
            time_range = {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31"
            }
            
            # Look for specific date mentions
            if "last month" in user_lower:
                time_range = {"start_date": "2024-06-01", "end_date": "2024-06-30"}
            elif "this year" in user_lower:
                time_range = {"start_date": "2024-01-01", "end_date": "2024-12-31"}
            elif "last 6 months" in user_lower:
                time_range = {"start_date": "2024-01-01", "end_date": "2024-06-30"}
            
            return {
                "workflow_id": "energy_analysis_workflow",
                "steps": [
                    {
                        "agent": "energy-monitoring",
                        "tool": "analyze_usage_patterns",
                        "parameters": {
                            "scope": "building",
                            "identifier": building_id,
                            "time_range": time_range
                        }
                    },
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "identify_optimization_opportunities",
                        "parameters": {
                            "buildings_list": [building_id],
                            "opportunity_types": ["LED", "HVAC", "Solar"],
                            "min_roi_threshold": 1.2,
                            "max_payback_years": 7
                        }
                    }
                ]
            }
        
        # Handle portfolio performance/metrics requests specifically
        elif any(word in user_lower for word in ["performance", "metrics", "benchmark", "sustainability"]):
            return {
                "workflow_id": "portfolio_performance_workflow",
                "steps": [
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "analyze_portfolio_energy_usage",
                        "parameters": {
                            "portfolio_id": "portfolio_001",
                            "date_range": {
                                "start_date": "2024-01-01",
                                "end_date": "2024-12-31"
                            }
                        }
                    },
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "benchmark_portfolio_performance",
                        "parameters": {
                            "portfolio_id": "portfolio_001",
                            "benchmark_type": "industry"
                        }
                    },
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "generate_sustainability_report",
                        "parameters": {
                            "portfolio_id": "portfolio_001",
                            "reporting_period": {
                                "start_date": "2024-01-01",
                                "end_date": "2024-12-31"
                            },
                            "report_type": "executive"
                        }
                    }
                ]
            }
        
        # Handle portfolio analysis requests
        elif any(word in user_lower for word in ["portfolio", "buildings", "facilities"]):
            # Extract portfolio ID if mentioned
            portfolio_id = "portfolio_001"  # Default
            portfolio_match = re.search(r'portfolio\s+([a-zA-Z0-9_]+)', user_lower)
            if portfolio_match:
                portfolio_id = portfolio_match.group(1)
            
            # Extract date range
            date_range = {"start_date": "2024-01-01", "end_date": "2024-12-31"}
            if "last quarter" in user_lower:
                date_range = {"start_date": "2024-04-01", "end_date": "2024-06-30"}
            elif "this quarter" in user_lower:
                date_range = {"start_date": "2024-07-01", "end_date": "2024-09-30"}
            
            return {
                "workflow_id": "portfolio_analysis_workflow",
                "steps": [
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "analyze_portfolio_energy_usage",
                        "parameters": {
                            "portfolio_id": portfolio_id,
                            "date_range": date_range
                        }
                    },
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "benchmark_portfolio_performance",
                        "parameters": {
                            "portfolio_id": portfolio_id,
                            "benchmark_type": "industry_comparison"
                        }
                    }
                ]
            }
        
        # Handle financial analysis requests
        elif any(word in user_lower for word in ["finance", "roi", "cost", "savings"]):
            # Extract project type if mentioned
            project_type = "LED"  # Default
            if "led" in user_lower:
                project_type = "LED"
            elif "hvac" in user_lower:
                project_type = "HVAC"
            elif "solar" in user_lower:
                project_type = "Solar"
            elif "storage" in user_lower:
                project_type = "Storage"
            elif "controls" in user_lower:
                project_type = "Controls"
            
            # Extract building number if mentioned
            building_id = "building_123"  # Default
            building_match = re.search(r'building\s+(\d+)', user_lower)
            if building_match:
                building_id = f"building_{building_match.group(1)}"
            
            return {
                "workflow_id": "financial_analysis_workflow",
                "steps": [
                    {
                        "agent": "energy-finance",
                        "tool": "calculate_project_roi",
                        "parameters": {
                            "project_details": {
                                "project_name": f"{project_type} Retrofit for {building_id}",
                                "technology_type": project_type,
                                "total_investment": 50000,
                                "installation_cost": 10000,
                                "equipment_cost": 40000,
                                "project_lifetime": 15
                            },
                            "energy_savings": {
                                "annual_kwh_savings": 50000,
                                "annual_gas_savings": 1000,
                                "demand_reduction_kw": 50,
                                "baseline_energy_cost": 75000
                            },
                            "financial_parameters": {
                                "discount_rate": 0.08,
                                "electricity_rate": 0.12,
                                "gas_rate": 0.85,
                                "inflation_rate": 0.025
                            }
                        }
                    },
                    {
                        "agent": "energy-finance",
                        "tool": "optimize_eaas_contract",
                        "parameters": {
                            "contract_parameters": {
                                "contract_term": 10,
                                "guaranteed_savings": 50000,
                                "base_year_consumption": 100000,
                                "sharing_percentage": 0.7,
                                "performance_threshold": 0.9
                            },
                            "project_costs": {
                                "capital_cost": 50000,
                                "operating_costs": 5000,
                                "maintenance_costs": 3000
                            },
                            "optimization_objectives": ["maximize_npv", "minimize_risk"]
                        }
                    }
                ]
            }
        
        # Handle document processing requests
        elif any(word in user_lower for word in ["document", "pdf", "report", "summarize"]):
            return {
                "workflow_id": "document_processing_workflow",
                "steps": [
                    {
                        "agent": "document-processing",
                        "tool": "extract_text",
                        "parameters": {
                            "document_type": "utility_bill",
                            "extraction_mode": "full_text"
                        }
                    },
                    {
                        "agent": "summarize",
                        "tool": "summarize_text",
                        "parameters": {
                            "summary_length": "medium",
                            "focus_areas": ["key_insights", "recommendations"]
                        }
                    }
                ]
            }
        
        # Default workflow for general requests
        else:
            return {
                "workflow_id": "general_analysis_workflow",
                "steps": [
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "search_facilities",
                        "parameters": {
                            "location": "all",
                            "facility_type": None,
                            "min_capacity": None,
                            "max_capacity": None
                        }
                    }
                ]
            }