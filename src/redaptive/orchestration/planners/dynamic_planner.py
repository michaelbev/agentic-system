"""Dynamic workflow planner."""

import re
from typing import Dict, List, Any
from .base_planner import BasePlanner
from ..matchers import KeywordMatcher

class DynamicPlanner(BasePlanner):
    """Dynamic planner that adapts workflows based on context."""
    
    def __init__(self):
        super().__init__()
        # Initialize the keyword matcher for intent detection
        self.keyword_matcher = KeywordMatcher()
        
        # Common company name mappings for quick lookup
        self.company_portfolio_map = {
            "walmart": "PORTFOLIO-002",
            "microsoft": "PORTFOLIO-001", 
            "jpmorgan": "PORTFOLIO-003",
            "jp": "PORTFOLIO-003",
            "general motors": "PORTFOLIO-004",
            "gm": "PORTFOLIO-004",
            "amazon": "PORTFOLIO-005"
        }
        
        # Default date ranges for different time periods
        self.date_ranges = {
            "current_year": {"start_date": "2025-01-01", "end_date": "2025-12-31"},
            "last_year": {"start_date": "2024-01-01", "end_date": "2024-12-31"},
            "last_quarter": {"start_date": "2025-04-01", "end_date": "2025-06-30"},
            "this_quarter": {"start_date": "2025-07-01", "end_date": "2025-09-30"},
            "last_month": {"start_date": "2025-06-01", "end_date": "2025-06-30"},
            "last_6_months": {"start_date": "2025-01-01", "end_date": "2025-06-30"}
        }
    
    async def create_workflow(self, user_request: str, 
                            available_agents: List[str]) -> Dict[str, Any]:
        """Create a workflow plan from user request."""
        
        # Validate available agents
        if not available_agents:
            return {"workflow_id": "no_agents_workflow", "steps": []}
        
        # Use the keyword matcher for intent detection
        intent_result = await self.keyword_matcher.match_intent(user_request)
        intent = intent_result.get('intent', 'unknown')
        confidence = intent_result.get('confidence', 0.0)
        all_matches = intent_result.get('all_matches', {})
        
        # Determine workflow type based on user request
        user_lower = user_request.lower()
        
        # Handle out-of-scope requests
        if intent == "out_of_scope":
            return {
                "workflow_id": "out_of_scope_workflow",
                "planning_method": "rule_based",
                "planning_reason": f"Out-of-scope query detected via keyword matcher. Intent: '{intent}', Confidence: {confidence:.2f}. Reason: {intent_result.get('reason', 'N/A')}. System domain: Energy-as-a-Service (EaaS) portfolio management and optimization.",
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
        
        # Handle energy-specific date/time queries (like "what is the date of the most recent energy usage reading?")
        if intent == "energy_monitoring" and any(word in user_lower for word in ["date", "time", "when", "latest", "recent", "most recent"]):
            return {
                "workflow_id": "energy_monitoring_date_workflow",
                "planning_method": "rule_based",
                "planning_reason": f"Energy-specific date query detected via keyword matcher. Intent: '{intent}', Confidence: {confidence:.2f}. All matches: {all_matches}. Routing to energy-monitoring agent for latest reading data.",
                "steps": [
                    {
                        "agent": "energy-monitoring",
                        "tool": "get_latest_energy_reading",
                        "parameters": {
                            "include_details": True
                        }
                    }
                ]
            }
        
        # Handle general time/date requests (not energy-specific)
        if intent == "time":
            return {
                "workflow_id": "time_analysis_workflow",
                "planning_method": "rule_based",
                "planning_reason": f"General time/date query detected via keyword matcher. Intent: '{intent}', Confidence: {confidence:.2f}. All matches: {all_matches}. Routing to system agent for current time information.",
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
        if intent == "energy":
            # Extract building identifier dynamically
            building_id = None
            building_match = re.search(r'building\s+(\d+)', user_lower)
            if building_match:
                building_id = f"building_{building_match.group(1)}"
            else:
                # Look for other building identifiers
                building_match = re.search(r'(\w+)\s+building', user_lower)
                if building_match:
                    building_id = building_match.group(1)
                else:
                    building_id = "default_building"  # Generic fallback
            
            # Extract date range dynamically
            time_range = self.date_ranges["current_year"]  # Default to current year
            time_period_detected = "current_year"
            
            # Look for specific date mentions
            if "last month" in user_lower:
                time_range = self.date_ranges["last_month"]
                time_period_detected = "last_month"
            elif "this year" in user_lower:
                time_range = self.date_ranges["current_year"]
                time_period_detected = "current_year"
            elif "last 6 months" in user_lower:
                time_range = self.date_ranges["last_6_months"]
                time_period_detected = "last_6_months"
            elif "last quarter" in user_lower:
                time_range = self.date_ranges["last_quarter"]
                time_period_detected = "last_quarter"
            elif "this quarter" in user_lower:
                time_range = self.date_ranges["this_quarter"]
                time_period_detected = "this_quarter"
            elif "last year" in user_lower:
                time_range = self.date_ranges["last_year"]
                time_period_detected = "last_year"
            
            return {
                "workflow_id": "energy_analysis_workflow",
                "planning_method": "rule_based",
                "planning_reason": f"Energy analysis query detected via keyword matcher. Intent: '{intent}', Confidence: {confidence:.2f}. All matches: {all_matches}. Building ID extracted: '{building_id}'. Time period detected: '{time_period_detected}' ({time_range['start_date']} to {time_range['end_date']}). Routing to energy-monitoring agent for usage pattern analysis and portfolio-intelligence agent for optimization opportunities.",
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
        if intent == "portfolio" and any(word in user_lower for word in ["performance", "metrics", "benchmark", "sustainability"]):
            # Determine portfolio ID based on query content
            portfolio_id = "PORTFOLIO-002"  # Default to Walmart
            company_detected = "default"
            
            # Check for specific company mentions using the mapping
            for company, portfolio in self.company_portfolio_map.items():
                if company in user_lower:
                    portfolio_id = portfolio
                    company_detected = company
                    break
            
            return {
                "workflow_id": "portfolio_performance_workflow",
                "planning_method": "rule_based",
                "planning_reason": f"Portfolio performance query detected via keyword matcher. Intent: '{intent}', Confidence: {confidence:.2f}. All matches: {all_matches}. Company detected: '{company_detected}' -> Portfolio ID: '{portfolio_id}'. Routing to portfolio-intelligence agent for comprehensive performance analysis including energy usage, benchmarking, and sustainability reporting.",
                "steps": [
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "analyze_portfolio_energy_usage",
                        "parameters": {
                            "portfolio_id": portfolio_id,
                            "date_range": {
                                "start_date": "2025-01-01",
                                "end_date": "2025-12-31"
                            }
                        }
                    },
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "benchmark_portfolio_performance",
                        "parameters": {
                            "portfolio_id": portfolio_id,
                            "benchmark_type": "industry"
                        }
                    },
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "generate_sustainability_report",
                        "parameters": {
                            "portfolio_id": portfolio_id,
                            "reporting_period": {
                                "start_date": "2025-01-01",
                                "end_date": "2025-12-31"
                            },
                            "report_type": "executive"
                        }
                    }
                ]
            }
        
        # Handle portfolio analysis requests
        if intent == "portfolio":
            # Extract portfolio ID dynamically
            portfolio_id = None
            company_detected = "none"
            
            # Check for specific company mentions using the mapping
            for company, portfolio in self.company_portfolio_map.items():
                if company in user_lower:
                    portfolio_id = portfolio
                    company_detected = company
                    break
            
            # Extract explicit portfolio ID if mentioned
            portfolio_match = re.search(r'portfolio\s+([a-zA-Z0-9_-]+)', user_lower)
            if portfolio_match:
                portfolio_id = portfolio_match.group(1).upper()
                company_detected = "explicit_portfolio_id"
            
            # If no specific portfolio identified, use a generic approach
            if not portfolio_id:
                portfolio_id = "PORTFOLIO-002"  # Fallback for testing
                company_detected = "default_fallback"
            
            # Extract date range dynamically
            date_range = self.date_ranges["current_year"]  # Default to current year
            time_period_detected = "current_year"
            
            # Look for specific time periods
            if "last quarter" in user_lower:
                date_range = self.date_ranges["last_quarter"]
                time_period_detected = "last_quarter"
            elif "this quarter" in user_lower:
                date_range = self.date_ranges["this_quarter"]
                time_period_detected = "this_quarter"
            elif "last month" in user_lower:
                date_range = self.date_ranges["last_month"]
                time_period_detected = "last_month"
            elif "this year" in user_lower:
                date_range = self.date_ranges["current_year"]
                time_period_detected = "current_year"
            elif "last year" in user_lower:
                date_range = self.date_ranges["last_year"]
                time_period_detected = "last_year"
            elif "last 6 months" in user_lower:
                date_range = self.date_ranges["last_6_months"]
                time_period_detected = "last_6_months"
            
            return {
                "workflow_id": "portfolio_analysis_workflow",
                "planning_method": "rule_based",
                "planning_reason": f"Portfolio analysis query detected via keyword matcher. Intent: '{intent}', Confidence: {confidence:.2f}. All matches: {all_matches}. Company detection: '{company_detected}' -> Portfolio ID: '{portfolio_id}'. Time period detected: '{time_period_detected}' ({date_range['start_date']} to {date_range['end_date']}). Routing to portfolio-intelligence agent for energy usage analysis and benchmarking.",
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
        if intent == "finance":
            # Extract project type dynamically
            project_type = "LED"  # Default
            project_type_keywords = ["led", "hvac", "solar", "storage", "controls"]
            found_project_type = None
            
            for keyword in project_type_keywords:
                if keyword in user_lower:
                    project_type = keyword.upper() if keyword != "led" else "LED"
                    found_project_type = keyword
                    break
            
            # Extract building identifier dynamically
            building_id = None
            building_match = re.search(r'building\s+(\d+)', user_lower)
            if building_match:
                building_id = f"building_{building_match.group(1)}"
            else:
                # Look for other building identifiers
                building_match = re.search(r'(\w+)\s+building', user_lower)
                if building_match:
                    building_id = building_match.group(1)
                else:
                    building_id = "default_building"  # Generic fallback
            
            # Extract financial parameters from query context
            investment_amount = None
            investment_match = re.search(r'\$?(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:k|thousand|k\s*dollars)', user_lower)
            if investment_match:
                investment_amount = float(investment_match.group(1).replace(',', '')) * 1000
            else:
                investment_match = re.search(r'\$?(\d+(?:,\d+)*(?:\.\d+)?)', user_lower)
                if investment_match:
                    investment_amount = float(investment_match.group(1).replace(',', ''))
            
            # Use reasonable defaults if no specific amounts mentioned
            if not investment_amount:
                investment_amount = 50000  # Default for demonstration
            
            return {
                "workflow_id": "financial_analysis_workflow",
                "planning_method": "rule_based",
                "planning_reason": f"Financial/ROI query detected via keyword matcher. Intent: '{intent}', Confidence: {confidence:.2f}. All matches: {all_matches}. Project type detected: '{found_project_type or 'default LED'}'. Building ID extracted: '{building_id}'. Investment amount extracted: ${investment_amount:,.0f}. Routing to energy-finance agent for ROI calculation and EaaS contract optimization.",
                "steps": [
                    {
                        "agent": "energy-finance",
                        "tool": "calculate_project_roi",
                        "parameters": {
                            "project_details": {
                                "project_name": f"{project_type} Retrofit for {building_id}",
                                "technology_type": project_type,
                                "total_investment": investment_amount,
                                "installation_cost": investment_amount * 0.2,  # 20% of total
                                "equipment_cost": investment_amount * 0.8,    # 80% of total
                                "project_lifetime": 15
                            },
                            "energy_savings": {
                                "annual_kwh_savings": investment_amount * 0.1,  # Estimate based on investment
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
                                "guaranteed_savings": investment_amount * 0.15,  # 15% annual savings
                                "base_year_consumption": 100000,
                                "sharing_percentage": 0.7,
                                "performance_threshold": 0.9
                            },
                            "project_costs": {
                                "capital_cost": investment_amount,
                                "operating_costs": investment_amount * 0.1,  # 10% of investment
                                "maintenance_costs": investment_amount * 0.06  # 6% of investment
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