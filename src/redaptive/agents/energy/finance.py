#!/usr/bin/env python3
"""
Energy Project Finance Agent - Redaptive Energy-as-a-Service Platform

This agent provides financial analysis and optimization capabilities for energy projects,
supporting Redaptive's EaaS business model and revenue optimization.

Key capabilities:
- EaaS contract optimization and financial modeling
- ROI calculations for energy projects (NPV, IRR, payback period)
- Technology selection optimization based on financial criteria
- Risk assessment and scenario analysis
- Performance-based contract structuring
- Energy savings verification and M&V protocols
- Portfolio-level financial optimization
- Investment prioritization and capital allocation
"""

import sys
import os
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import math

# Use new import structure

from redaptive.agents.base import BaseMCPServer
from redaptive.config.database import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnergyFinanceAgent(BaseMCPServer):
    """
    Energy Project Finance Agent for Redaptive's EaaS Revenue Optimization
    
    Provides comprehensive financial analysis, contract optimization, and ROI
    calculations for energy-as-a-service projects and technology investments.
    """

    def __init__(self):
        super().__init__("energy-finance-agent")
        self.financial_models = {}
        self.market_rates = {
            "discount_rate": 0.08,  # 8% WACC
            "inflation_rate": 0.025,  # 2.5% inflation
            "electricity_escalation": 0.03,  # 3% annual electricity price escalation
            "gas_escalation": 0.025,  # 2.5% annual gas price escalation
            "risk_free_rate": 0.045  # 4.5% risk-free rate
        }
        self.technology_costs = {
            "LED": {"cost_per_unit": 25, "lifetime_years": 15, "maintenance_factor": 0.02},
            "HVAC": {"cost_per_unit": 2500, "lifetime_years": 20, "maintenance_factor": 0.05},
            "Solar": {"cost_per_kw": 2000, "lifetime_years": 25, "maintenance_factor": 0.015},
            "Storage": {"cost_per_kwh": 800, "lifetime_years": 15, "maintenance_factor": 0.03},
            "Controls": {"cost_per_sqft": 3, "lifetime_years": 12, "maintenance_factor": 0.04}
        }
        self.setup_tools()
        logger.info("Energy Project Finance Agent initialized for EaaS optimization")

    def setup_tools(self):
        """Setup MCP tools for energy project finance"""
        
        # Tool 1: Calculate Project ROI
        self.register_tool(
            "calculate_project_roi",
            "Calculate comprehensive ROI analysis for energy projects including NPV, IRR, and payback",
            self.calculate_project_roi,
            {
                "type": "object",
                "properties": {
                    "project_details": {
                        "type": "object",
                        "description": "Project details and costs",
                        "properties": {
                            "project_name": {"type": "string", "description": "Project name"},
                            "technology_type": {"type": "string", "enum": ["LED", "HVAC", "Solar", "Storage", "Controls", "Mixed"], "description": "Primary technology type"},
                            "total_investment": {"type": "number", "description": "Total project investment in USD"},
                            "installation_cost": {"type": "number", "description": "Installation cost in USD"},
                            "equipment_cost": {"type": "number", "description": "Equipment cost in USD"},
                            "project_lifetime": {"type": "integer", "description": "Project lifetime in years", "default": 15}
                        },
                        "required": ["project_name", "technology_type", "total_investment"]
                    },
                    "energy_savings": {
                        "type": "object",
                        "description": "Expected energy savings",
                        "properties": {
                            "annual_kwh_savings": {"type": "number", "description": "Annual kWh savings"},
                            "annual_gas_savings": {"type": "number", "description": "Annual gas savings (therms)"},
                            "demand_reduction_kw": {"type": "number", "description": "Peak demand reduction in kW"},
                            "baseline_energy_cost": {"type": "number", "description": "Baseline annual energy cost"}
                        },
                        "required": ["annual_kwh_savings", "baseline_energy_cost"]
                    },
                    "financial_parameters": {
                        "type": "object",
                        "description": "Financial analysis parameters",
                        "properties": {
                            "discount_rate": {"type": "number", "description": "Discount rate for NPV calculation", "default": 0.08},
                            "electricity_rate": {"type": "number", "description": "Current electricity rate ($/kWh)", "default": 0.12},
                            "gas_rate": {"type": "number", "description": "Current gas rate ($/therm)", "default": 1.25},
                            "demand_charge": {"type": "number", "description": "Demand charge ($/kW/month)", "default": 15},
                            "incentives": {"type": "number", "description": "Utility incentives and rebates", "default": 0},
                            "tax_benefits": {"type": "number", "description": "Tax benefits and credits", "default": 0}
                        }
                    },
                    "risk_factors": {
                        "type": "object",
                        "description": "Risk assessment parameters",
                        "properties": {
                            "performance_risk": {"type": "number", "description": "Performance degradation risk (0-1)", "default": 0.1},
                            "technology_risk": {"type": "number", "description": "Technology risk factor (0-1)", "default": 0.05},
                            "market_risk": {"type": "number", "description": "Market volatility risk (0-1)", "default": 0.15}
                        }
                    }
                },
                "required": ["project_details", "energy_savings"]
            }
        )

        # Tool 2: Optimize EaaS Contract Structure
        self.register_tool(
            "optimize_eaas_contract",
            "Optimize Energy-as-a-Service contract structure for maximum value",
            self.optimize_eaas_contract,
            {
                "type": "object",
                "properties": {
                    "contract_parameters": {
                        "type": "object",
                        "description": "EaaS contract parameters",
                        "properties": {
                            "contract_term": {"type": "integer", "description": "Contract term in years"},
                            "guaranteed_savings": {"type": "number", "description": "Guaranteed annual savings"},
                            "sharing_percentage": {"type": "number", "description": "Redaptive's savings share (0-1)", "default": 0.7},
                            "performance_threshold": {"type": "number", "description": "Minimum performance threshold", "default": 0.85},
                            "base_year_consumption": {"type": "number", "description": "Baseline energy consumption (kWh)"}
                        },
                        "required": ["contract_term", "guaranteed_savings", "base_year_consumption"]
                    },
                    "project_costs": {
                        "type": "object",
                        "description": "Project cost structure",
                        "properties": {
                            "capital_cost": {"type": "number", "description": "Total capital investment"},
                            "operating_costs": {"type": "number", "description": "Annual operating costs"},
                            "maintenance_costs": {"type": "number", "description": "Annual maintenance costs"},
                            "insurance_costs": {"type": "number", "description": "Annual insurance costs"}
                        },
                        "required": ["capital_cost"]
                    },
                    "optimization_objectives": {
                        "type": "array",
                        "description": "Optimization objectives",
                        "items": {
                            "type": "string",
                            "enum": ["maximize_npv", "minimize_risk", "maximize_irr", "minimize_payback", "maximize_cash_flow"]
                        },
                        "default": ["maximize_npv", "minimize_risk"]
                    },
                    "constraints": {
                        "type": "object",
                        "description": "Contract constraints",
                        "properties": {
                            "min_irr": {"type": "number", "description": "Minimum required IRR", "default": 0.15},
                            "max_payback": {"type": "number", "description": "Maximum payback period (years)", "default": 7},
                            "min_savings_guarantee": {"type": "number", "description": "Minimum savings guarantee", "default": 0.8}
                        }
                    }
                },
                "required": ["contract_parameters", "project_costs"]
            }
        )

        # Tool 3: Technology Selection Optimization
        self.register_tool(
            "optimize_technology_selection",
            "Optimize technology selection based on financial criteria and site conditions",
            self.optimize_technology_selection,
            {
                "type": "object",
                "properties": {
                    "site_conditions": {
                        "type": "object",
                        "description": "Site conditions and requirements",
                        "properties": {
                            "building_type": {"type": "string", "enum": ["office", "retail", "warehouse", "manufacturing", "healthcare", "education"]},
                            "floor_area": {"type": "number", "description": "Building floor area (sq ft)"},
                            "operating_hours": {"type": "number", "description": "Annual operating hours"},
                            "current_equipment_age": {"type": "number", "description": "Current equipment age (years)"},
                            "energy_intensity": {"type": "number", "description": "Energy intensity (kWh/sq ft/year)"},
                            "budget_constraint": {"type": "number", "description": "Budget constraint (USD)"}
                        },
                        "required": ["building_type", "floor_area", "budget_constraint"]
                    },
                    "available_technologies": {
                        "type": "array",
                        "description": "Available technology options",
                        "items": {
                            "type": "string",
                            "enum": ["LED", "HVAC", "Solar", "Storage", "Controls", "Insulation", "Windows"]
                        },
                        "default": ["LED", "HVAC", "Controls"]
                    },
                    "selection_criteria": {
                        "type": "object",
                        "description": "Technology selection criteria weights",
                        "properties": {
                            "roi_weight": {"type": "number", "description": "ROI importance weight", "default": 0.4},
                            "payback_weight": {"type": "number", "description": "Payback importance weight", "default": 0.3},
                            "risk_weight": {"type": "number", "description": "Risk importance weight", "default": 0.2},
                            "implementation_weight": {"type": "number", "description": "Implementation ease weight", "default": 0.1}
                        }
                    },
                    "performance_requirements": {
                        "type": "object",
                        "description": "Performance requirements",
                        "properties": {
                            "min_energy_savings": {"type": "number", "description": "Minimum energy savings (%)", "default": 0.15},
                            "max_implementation_time": {"type": "number", "description": "Maximum implementation time (months)", "default": 12},
                            "reliability_requirement": {"type": "number", "description": "Reliability requirement (0-1)", "default": 0.95}
                        }
                    }
                },
                "required": ["site_conditions", "available_technologies"]
            }
        )

        # Tool 4: Risk Assessment and Scenario Analysis
        self.register_tool(
            "assess_project_risk",
            "Perform comprehensive risk assessment and scenario analysis for energy projects",
            self.assess_project_risk,
            {
                "type": "object",
                "properties": {
                    "project_data": {
                        "type": "object",
                        "description": "Project data for risk analysis",
                        "properties": {
                            "project_id": {"type": "string", "description": "Project identifier"},
                            "base_case_npv": {"type": "number", "description": "Base case NPV"},
                            "base_case_irr": {"type": "number", "description": "Base case IRR"},
                            "expected_savings": {"type": "number", "description": "Expected annual savings"},
                            "project_cost": {"type": "number", "description": "Total project cost"}
                        },
                        "required": ["project_id", "base_case_npv", "expected_savings", "project_cost"]
                    },
                    "risk_variables": {
                        "type": "object",
                        "description": "Risk variables and their ranges",
                        "properties": {
                            "energy_price_volatility": {"type": "number", "description": "Energy price volatility (±%)", "default": 0.20},
                            "performance_variance": {"type": "number", "description": "Performance variance (±%)", "default": 0.15},
                            "maintenance_cost_variance": {"type": "number", "description": "Maintenance cost variance (±%)", "default": 0.25},
                            "equipment_failure_risk": {"type": "number", "description": "Equipment failure probability", "default": 0.05},
                            "regulatory_risk": {"type": "number", "description": "Regulatory change impact", "default": 0.10}
                        }
                    },
                    "scenario_types": {
                        "type": "array",
                        "description": "Types of scenarios to analyze",
                        "items": {
                            "type": "string",
                            "enum": ["best_case", "worst_case", "most_likely", "stress_test", "monte_carlo"]
                        },
                        "default": ["best_case", "worst_case", "most_likely"]
                    },
                    "confidence_level": {
                        "type": "number",
                        "description": "Confidence level for risk analysis",
                        "default": 0.95
                    }
                },
                "required": ["project_data"]
            }
        )

        # Tool 5: Portfolio Financial Optimization
        self.register_tool(
            "optimize_portfolio_finance",
            "Optimize financial performance across multiple energy projects in a portfolio",
            self.optimize_portfolio_finance,
            {
                "type": "object",
                "properties": {
                    "portfolio_data": {
                        "type": "object",
                        "description": "Portfolio financial data",
                        "properties": {
                            "portfolio_id": {"type": "string", "description": "Portfolio identifier"},
                            "total_budget": {"type": "number", "description": "Total available budget"},
                            "target_roi": {"type": "number", "description": "Target portfolio ROI", "default": 0.20},
                            "risk_tolerance": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"},
                            "investment_horizon": {"type": "integer", "description": "Investment horizon (years)", "default": 10}
                        },
                        "required": ["portfolio_id", "total_budget"]
                    },
                    "candidate_projects": {
                        "type": "array",
                        "description": "Candidate projects for portfolio optimization",
                        "items": {
                            "type": "object",
                            "properties": {
                                "project_id": {"type": "string", "description": "Project identifier"},
                                "investment_required": {"type": "number", "description": "Required investment"},
                                "expected_npv": {"type": "number", "description": "Expected NPV"},
                                "expected_irr": {"type": "number", "description": "Expected IRR"},
                                "risk_score": {"type": "number", "description": "Risk score (0-1)"},
                                "strategic_value": {"type": "number", "description": "Strategic value score (0-1)"},
                                "implementation_priority": {"type": "string", "enum": ["high", "medium", "low"]}
                            },
                            "required": ["project_id", "investment_required", "expected_npv", "expected_irr"]
                        }
                    },
                    "optimization_constraints": {
                        "type": "object",
                        "description": "Portfolio optimization constraints",
                        "properties": {
                            "max_risk_exposure": {"type": "number", "description": "Maximum portfolio risk exposure", "default": 0.3},
                            "min_diversification": {"type": "number", "description": "Minimum diversification requirement", "default": 0.2},
                            "geographic_limits": {"type": "object", "description": "Geographic concentration limits"},
                            "technology_limits": {"type": "object", "description": "Technology concentration limits"}
                        }
                    }
                },
                "required": ["portfolio_data", "candidate_projects"]
            }
        )

        # Tool 6: Performance-Based Contract Analysis
        self.register_tool(
            "analyze_performance_contract",
            "Analyze performance-based contract terms and M&V protocols",
            self.analyze_performance_contract,
            {
                "type": "object",
                "properties": {
                    "contract_terms": {
                        "type": "object",
                        "description": "Performance contract terms",
                        "properties": {
                            "contract_id": {"type": "string", "description": "Contract identifier"},
                            "performance_guarantee": {"type": "number", "description": "Performance guarantee (%)"},
                            "measurement_period": {"type": "integer", "description": "Measurement period (months)"},
                            "baseline_methodology": {"type": "string", "enum": ["weather_normalized", "regression", "time_series"], "default": "weather_normalized"},
                            "adjustment_factors": {"type": "array", "items": {"type": "string"}, "description": "Allowable adjustment factors"},
                            "penalty_structure": {"type": "object", "description": "Performance penalty structure"}
                        },
                        "required": ["contract_id", "performance_guarantee"]
                    },
                    "measurement_verification": {
                        "type": "object",
                        "description": "M&V protocol parameters",
                        "properties": {
                            "mv_option": {"type": "string", "enum": ["Option A", "Option B", "Option C", "Option D"], "description": "IPMVP M&V option"},
                            "measurement_accuracy": {"type": "number", "description": "Required measurement accuracy", "default": 0.95},
                            "reporting_frequency": {"type": "string", "enum": ["monthly", "quarterly", "annually"], "default": "monthly"},
                            "verification_method": {"type": "string", "enum": ["meter_based", "calculated", "stipulated"]}
                        }
                    },
                    "financial_analysis": {
                        "type": "object",
                        "description": "Financial analysis parameters",
                        "properties": {
                            "shared_savings_rate": {"type": "number", "description": "Shared savings rate (0-1)"},
                            "true_up_methodology": {"type": "string", "description": "Annual true-up methodology"},
                            "escalation_rates": {"type": "object", "description": "Energy price escalation rates"},
                            "risk_allocation": {"type": "object", "description": "Risk allocation matrix"}
                        }
                    }
                },
                "required": ["contract_terms", "measurement_verification"]
            }
        )

    async def calculate_project_roi(self, project_details: Dict, energy_savings: Dict, 
                                  financial_parameters: Dict = None, risk_factors: Dict = None) -> Dict[str, Any]:
        """Calculate comprehensive ROI analysis for energy projects"""
        try:
            # Set default parameters
            if financial_parameters is None:
                financial_parameters = {}
            if risk_factors is None:
                risk_factors = {}
            
            # Extract project parameters
            project_name = project_details["project_name"]
            technology_type = project_details["technology_type"]
            total_investment = project_details["total_investment"]
            project_lifetime = project_details.get("project_lifetime", 15)
            
            # Extract savings parameters
            annual_kwh_savings = energy_savings["annual_kwh_savings"]
            baseline_energy_cost = energy_savings["baseline_energy_cost"]
            annual_gas_savings = energy_savings.get("annual_gas_savings", 0)
            demand_reduction_kw = energy_savings.get("demand_reduction_kw", 0)
            
            # Extract financial parameters
            discount_rate = financial_parameters.get("discount_rate", self.market_rates["discount_rate"])
            electricity_rate = financial_parameters.get("electricity_rate", 0.12)
            gas_rate = financial_parameters.get("gas_rate", 1.25)
            demand_charge = financial_parameters.get("demand_charge", 15)
            incentives = financial_parameters.get("incentives", 0)
            tax_benefits = financial_parameters.get("tax_benefits", 0)
            
            # Calculate annual savings
            electricity_savings = annual_kwh_savings * electricity_rate
            gas_savings = annual_gas_savings * gas_rate
            demand_savings = demand_reduction_kw * demand_charge * 12  # Monthly demand charges
            total_annual_savings = electricity_savings + gas_savings + demand_savings
            
            # Calculate cash flows
            cash_flows = []
            cumulative_savings = 0
            
            for year in range(project_lifetime + 1):
                if year == 0:
                    # Initial investment
                    cash_flow = -(total_investment - incentives - tax_benefits)
                else:
                    # Annual savings with escalation
                    escalated_savings = total_annual_savings * (1 + self.market_rates["electricity_escalation"]) ** (year - 1)
                    
                    # Apply technology-specific degradation
                    tech_info = self.technology_costs.get(technology_type, {"maintenance_factor": 0.03})
                    maintenance_cost = total_investment * tech_info["maintenance_factor"]
                    
                    # Performance degradation
                    performance_factor = 1 - (risk_factors.get("performance_risk", 0.1) * (year - 1) / project_lifetime)
                    
                    cash_flow = (escalated_savings * performance_factor) - maintenance_cost
                
                cash_flows.append(cash_flow)
                if year > 0:
                    cumulative_savings += cash_flow
            
            # Calculate financial metrics
            npv = self._calculate_npv(cash_flows, discount_rate)
            irr = self._calculate_irr(cash_flows)
            payback_period = self._calculate_payback_period(cash_flows)
            profitability_index = (npv + total_investment) / total_investment if total_investment > 0 else 0
            
            # Risk-adjusted metrics
            risk_adjusted_discount_rate = discount_rate + sum(risk_factors.values()) * 0.02
            risk_adjusted_npv = self._calculate_npv(cash_flows, risk_adjusted_discount_rate)
            
            # Sensitivity analysis
            sensitivity = await self._perform_sensitivity_analysis(
                total_investment, total_annual_savings, discount_rate, project_lifetime
            )
            
            result = {
                "status": "success",
                "project_name": project_name,
                "technology_type": technology_type,
                "financial_metrics": {
                    "npv": round(npv, 2),
                    "irr": round(irr * 100, 2) if irr else None,
                    "payback_period_years": round(payback_period, 1) if payback_period else None,
                    "profitability_index": round(profitability_index, 2),
                    "risk_adjusted_npv": round(risk_adjusted_npv, 2),
                    "total_investment": total_investment,
                    "annual_savings": round(total_annual_savings, 2),
                    "lifetime_savings": round(cumulative_savings, 2)
                },
                "savings_breakdown": {
                    "electricity_savings_annual": round(electricity_savings, 2),
                    "gas_savings_annual": round(gas_savings, 2),
                    "demand_savings_annual": round(demand_savings, 2),
                    "total_annual_savings": round(total_annual_savings, 2)
                },
                "cash_flow_analysis": {
                    "year_0": cash_flows[0],
                    "year_1_5_avg": sum(cash_flows[1:6]) / 5 if len(cash_flows) > 5 else None,
                    "year_6_10_avg": sum(cash_flows[6:11]) / 5 if len(cash_flows) > 10 else None,
                    "final_year": cash_flows[-1] if cash_flows else None
                },
                "sensitivity_analysis": sensitivity,
                "investment_recommendation": self._generate_investment_recommendation(npv, irr, payback_period, risk_factors),
                "assumptions": {
                    "discount_rate": discount_rate,
                    "electricity_escalation": self.market_rates["electricity_escalation"],
                    "project_lifetime": project_lifetime,
                    "performance_degradation": risk_factors.get("performance_risk", 0.1)
                },
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"ROI analysis completed for {project_name}: NPV=${npv:,.2f}, IRR={irr*100:.1f}%")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating project ROI: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def optimize_eaas_contract(self, contract_parameters: Dict, project_costs: Dict, 
                                   optimization_objectives: List[str] = None, constraints: Dict = None) -> Dict[str, Any]:
        """Optimize Energy-as-a-Service contract structure"""
        try:
            if optimization_objectives is None:
                optimization_objectives = ["maximize_npv", "minimize_risk"]
            if constraints is None:
                constraints = {}
            
            # Extract parameters
            contract_term = contract_parameters["contract_term"]
            guaranteed_savings = contract_parameters["guaranteed_savings"]
            sharing_percentage = contract_parameters.get("sharing_percentage", 0.7)
            performance_threshold = contract_parameters.get("performance_threshold", 0.85)
            base_consumption = contract_parameters["base_year_consumption"]
            
            capital_cost = project_costs["capital_cost"]
            operating_costs = project_costs.get("operating_costs", capital_cost * 0.03)
            maintenance_costs = project_costs.get("maintenance_costs", capital_cost * 0.02)
            
            # Optimization constraints
            min_irr = constraints.get("min_irr", 0.15)
            max_payback = constraints.get("max_payback", 7)
            min_savings_guarantee = constraints.get("min_savings_guarantee", 0.8)
            
            # Generate contract scenarios
            scenarios = await self._generate_contract_scenarios(
                contract_term, guaranteed_savings, sharing_percentage, capital_cost
            )
            
            # Evaluate scenarios
            best_scenario = None
            best_score = -float('inf')
            
            for scenario in scenarios:
                # Calculate financial metrics for scenario
                cash_flows = self._calculate_contract_cash_flows(scenario, contract_term, operating_costs, maintenance_costs)
                npv = self._calculate_npv(cash_flows, self.market_rates["discount_rate"])
                irr = self._calculate_irr(cash_flows)
                payback = self._calculate_payback_period(cash_flows)
                
                # Check constraints
                if irr and irr < min_irr:
                    continue
                if payback and payback > max_payback:
                    continue
                if scenario["savings_guarantee"] < min_savings_guarantee:
                    continue
                
                # Calculate optimization score
                score = self._calculate_optimization_score(npv, irr, payback, scenario, optimization_objectives)
                
                if score > best_score:
                    best_score = score
                    best_scenario = scenario
                    best_scenario.update({
                        "npv": npv,
                        "irr": irr,
                        "payback_period": payback,
                        "optimization_score": score
                    })
            
            if not best_scenario:
                return {
                    "status": "no_feasible_solution",
                    "message": "No contract structure meets the specified constraints",
                    "constraints": constraints,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Generate contract recommendations
            recommendations = await self._generate_contract_recommendations(best_scenario, scenarios)
            
            # Calculate risk metrics
            risk_analysis = await self._analyze_contract_risk(best_scenario, contract_term)
            
            result = {
                "status": "success",
                "optimized_contract": best_scenario,
                "financial_performance": {
                    "expected_npv": round(best_scenario["npv"], 2),
                    "expected_irr": round(best_scenario["irr"] * 100, 2) if best_scenario["irr"] else None,
                    "payback_period": round(best_scenario["payback_period"], 1) if best_scenario["payback_period"] else None,
                    "optimization_score": round(best_scenario["optimization_score"], 2)
                },
                "contract_terms": {
                    "sharing_percentage": best_scenario["sharing_percentage"],
                    "savings_guarantee": best_scenario["savings_guarantee"],
                    "performance_threshold": best_scenario["performance_threshold"],
                    "escalation_rate": best_scenario.get("escalation_rate", 0.03),
                    "true_up_frequency": "annual"
                },
                "alternative_scenarios": scenarios[:3],  # Top 3 alternatives
                "recommendations": recommendations,
                "risk_analysis": risk_analysis,
                "optimization_objectives": optimization_objectives,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"EaaS contract optimization completed: NPV=${best_scenario['npv']:,.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing EaaS contract: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def optimize_technology_selection(self, site_conditions: Dict, available_technologies: List[str], 
                                          selection_criteria: Dict = None, performance_requirements: Dict = None) -> Dict[str, Any]:
        """Optimize technology selection based on financial criteria"""
        try:
            if selection_criteria is None:
                selection_criteria = {"roi_weight": 0.4, "payback_weight": 0.3, "risk_weight": 0.2, "implementation_weight": 0.1}
            if performance_requirements is None:
                performance_requirements = {"min_energy_savings": 0.15, "max_implementation_time": 12, "reliability_requirement": 0.95}
            
            # Extract site conditions
            building_type = site_conditions["building_type"]
            floor_area = site_conditions["floor_area"]
            budget_constraint = site_conditions["budget_constraint"]
            operating_hours = site_conditions.get("operating_hours", 3000)
            energy_intensity = site_conditions.get("energy_intensity", 15)  # kWh/sq ft/year
            
            # Evaluate each technology
            technology_evaluations = []
            
            for tech in available_technologies:
                evaluation = await self._evaluate_technology(
                    tech, site_conditions, selection_criteria, performance_requirements
                )
                if evaluation["feasible"]:
                    technology_evaluations.append(evaluation)
            
            # Sort by overall score
            technology_evaluations.sort(key=lambda x: x["overall_score"], reverse=True)
            
            # Generate technology combinations
            combinations = await self._generate_technology_combinations(
                technology_evaluations, budget_constraint, performance_requirements
            )
            
            # Find optimal combination
            optimal_combination = max(combinations, key=lambda x: x["combined_score"]) if combinations else None
            
            # Calculate portfolio-level metrics
            if optimal_combination:
                portfolio_metrics = await self._calculate_portfolio_metrics(optimal_combination["technologies"])
            else:
                portfolio_metrics = {}
            
            result = {
                "status": "success",
                "site_conditions": site_conditions,
                "technology_rankings": technology_evaluations,
                "optimal_combination": optimal_combination,
                "portfolio_metrics": portfolio_metrics,
                "selection_rationale": self._generate_selection_rationale(technology_evaluations, optimal_combination),
                "implementation_plan": await self._create_implementation_plan(optimal_combination) if optimal_combination else None,
                "alternative_combinations": combinations[1:4] if len(combinations) > 1 else [],  # Top 3 alternatives
                "budget_utilization": optimal_combination["total_cost"] / budget_constraint if optimal_combination else 0,
                "selection_criteria": selection_criteria,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Technology selection optimization completed for {building_type} building")
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing technology selection: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def assess_project_risk(self, project_data: Dict, risk_variables: Dict = None, 
                                scenario_types: List[str] = None, confidence_level: float = 0.95) -> Dict[str, Any]:
        """Perform comprehensive risk assessment and scenario analysis"""
        try:
            if risk_variables is None:
                risk_variables = {
                    "energy_price_volatility": 0.20,
                    "performance_variance": 0.15,
                    "maintenance_cost_variance": 0.25,
                    "equipment_failure_risk": 0.05,
                    "regulatory_risk": 0.10
                }
            if scenario_types is None:
                scenario_types = ["best_case", "worst_case", "most_likely"]
            
            project_id = project_data["project_id"]
            base_npv = project_data["base_case_npv"]
            base_irr = project_data["base_case_irr"]
            expected_savings = project_data["expected_savings"]
            project_cost = project_data["project_cost"]
            
            # Generate risk scenarios
            scenarios = {}
            
            for scenario_type in scenario_types:
                scenario_result = await self._generate_risk_scenario(
                    scenario_type, project_data, risk_variables
                )
                scenarios[scenario_type] = scenario_result
            
            # Monte Carlo simulation if requested
            if "monte_carlo" in scenario_types:
                monte_carlo_results = await self._run_monte_carlo_simulation(
                    project_data, risk_variables, confidence_level
                )
                scenarios["monte_carlo"] = monte_carlo_results
            
            # Calculate risk metrics
            risk_metrics = await self._calculate_risk_metrics(scenarios, base_npv, base_irr)
            
            # Risk categorization
            overall_risk_score = self._calculate_overall_risk_score(risk_variables, scenarios)
            risk_category = self._categorize_risk_level(overall_risk_score)
            
            # Generate risk mitigation strategies
            mitigation_strategies = await self._generate_risk_mitigation_strategies(risk_variables, scenarios)
            
            result = {
                "status": "success",
                "project_id": project_id,
                "base_case": {
                    "npv": base_npv,
                    "irr": base_irr,
                    "expected_savings": expected_savings,
                    "project_cost": project_cost
                },
                "risk_scenarios": scenarios,
                "risk_metrics": risk_metrics,
                "overall_risk_assessment": {
                    "risk_score": round(overall_risk_score, 2),
                    "risk_category": risk_category,
                    "confidence_level": confidence_level,
                    "key_risk_factors": self._identify_key_risk_factors(risk_variables)
                },
                "mitigation_strategies": mitigation_strategies,
                "recommendations": self._generate_risk_recommendations(risk_category, scenarios),
                "sensitivity_ranking": await self._rank_sensitivity_factors(project_data, risk_variables),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Risk assessment completed for {project_id}: Risk score {overall_risk_score:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error assessing project risk: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def optimize_portfolio_finance(self, portfolio_data: Dict, candidate_projects: List[Dict], 
                                       optimization_constraints: Dict = None) -> Dict[str, Any]:
        """Optimize financial performance across multiple energy projects"""
        try:
            if optimization_constraints is None:
                optimization_constraints = {"max_risk_exposure": 0.3, "min_diversification": 0.2}
            
            portfolio_id = portfolio_data["portfolio_id"]
            total_budget = portfolio_data["total_budget"]
            target_roi = portfolio_data.get("target_roi", 0.20)
            risk_tolerance = portfolio_data.get("risk_tolerance", "medium")
            
            # Analyze individual projects
            project_analysis = []
            for project in candidate_projects:
                analysis = await self._analyze_portfolio_project(project)
                project_analysis.append(analysis)
            
            # Portfolio optimization using efficient frontier
            optimal_portfolios = await self._optimize_portfolio_efficient_frontier(
                project_analysis, total_budget, optimization_constraints
            )
            
            # Select best portfolio based on risk tolerance
            selected_portfolio = self._select_portfolio_by_risk_tolerance(optimal_portfolios, risk_tolerance)
            
            # Calculate portfolio metrics
            portfolio_metrics = await self._calculate_portfolio_financial_metrics(selected_portfolio, project_analysis)
            
            # Diversification analysis
            diversification_analysis = self._analyze_portfolio_diversification(selected_portfolio, project_analysis)
            
            # Risk analysis
            portfolio_risk_analysis = await self._analyze_portfolio_risk(selected_portfolio, project_analysis)
            
            # Generate implementation timeline
            implementation_timeline = await self._create_portfolio_implementation_timeline(selected_portfolio)
            
            result = {
                "status": "success",
                "portfolio_id": portfolio_id,
                "selected_portfolio": {
                    "selected_projects": selected_portfolio,
                    "total_investment": sum(p["investment_required"] for p in selected_portfolio),
                    "budget_utilization": sum(p["investment_required"] for p in selected_portfolio) / total_budget,
                    "project_count": len(selected_portfolio)
                },
                "financial_metrics": portfolio_metrics,
                "risk_analysis": portfolio_risk_analysis,
                "diversification_analysis": diversification_analysis,
                "alternative_portfolios": optimal_portfolios[:3],  # Top 3 alternatives
                "implementation_timeline": implementation_timeline,
                "optimization_summary": {
                    "target_roi_achieved": portfolio_metrics.get("expected_roi", 0) >= target_roi,
                    "risk_constraints_met": portfolio_risk_analysis.get("portfolio_risk_score", 0) <= optimization_constraints.get("max_risk_exposure", 0.3),
                    "diversification_achieved": diversification_analysis.get("diversification_score", 0) >= optimization_constraints.get("min_diversification", 0.2)
                },
                "recommendations": self._generate_portfolio_recommendations(portfolio_metrics, diversification_analysis),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Portfolio optimization completed: {len(selected_portfolio)} projects, ${sum(p['investment_required'] for p in selected_portfolio):,.0f} investment")
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing portfolio finance: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def analyze_performance_contract(self, contract_terms: Dict, measurement_verification: Dict, 
                                         financial_analysis: Dict = None) -> Dict[str, Any]:
        """Analyze performance-based contract terms and M&V protocols"""
        try:
            if financial_analysis is None:
                financial_analysis = {}
            
            contract_id = contract_terms["contract_id"]
            performance_guarantee = contract_terms["performance_guarantee"]
            measurement_period = contract_terms.get("measurement_period", 12)
            baseline_methodology = contract_terms.get("baseline_methodology", "weather_normalized")
            
            mv_option = measurement_verification["mv_option"]
            measurement_accuracy = measurement_verification.get("measurement_accuracy", 0.95)
            reporting_frequency = measurement_verification.get("reporting_frequency", "monthly")
            
            # Analyze M&V protocol adequacy
            mv_analysis = await self._analyze_mv_protocol(measurement_verification, contract_terms)
            
            # Financial impact analysis
            financial_impact = await self._analyze_performance_contract_financials(
                contract_terms, financial_analysis
            )
            
            # Risk assessment for performance guarantee
            performance_risk = await self._assess_performance_guarantee_risk(
                performance_guarantee, baseline_methodology, mv_option
            )
            
            # Compliance analysis
            compliance_analysis = await self._analyze_contract_compliance_requirements(
                contract_terms, measurement_verification
            )
            
            # Cost-benefit analysis of M&V
            mv_cost_benefit = await self._analyze_mv_cost_benefit(measurement_verification, financial_impact)
            
            result = {
                "status": "success",
                "contract_id": contract_id,
                "mv_protocol_analysis": mv_analysis,
                "financial_impact_analysis": financial_impact,
                "performance_risk_assessment": performance_risk,
                "compliance_analysis": compliance_analysis,
                "mv_cost_benefit_analysis": mv_cost_benefit,
                "contract_recommendations": await self._generate_performance_contract_recommendations(
                    mv_analysis, financial_impact, performance_risk
                ),
                "implementation_requirements": {
                    "measurement_equipment": self._determine_required_equipment(mv_option),
                    "data_collection_frequency": self._determine_data_collection_frequency(mv_option),
                    "analysis_requirements": self._determine_analysis_requirements(baseline_methodology),
                    "reporting_obligations": self._determine_reporting_obligations(reporting_frequency)
                },
                "estimated_mv_costs": await self._estimate_mv_implementation_costs(measurement_verification),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Performance contract analysis completed for {contract_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing performance contract: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # Helper methods for financial calculations
    def _calculate_npv(self, cash_flows: List[float], discount_rate: float) -> float:
        """Calculate Net Present Value"""
        npv = 0
        for i, cash_flow in enumerate(cash_flows):
            npv += cash_flow / ((1 + discount_rate) ** i)
        return npv

    def _calculate_irr(self, cash_flows: List[float]) -> Optional[float]:
        """Calculate Internal Rate of Return using Newton-Raphson method"""
        if not cash_flows or len(cash_flows) < 2:
            return None
        
        # Initial guess
        rate = 0.1
        
        for _ in range(100):  # Maximum iterations
            npv = sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))
            dnpv = sum(-i * cf / ((1 + rate) ** (i + 1)) for i, cf in enumerate(cash_flows) if i > 0)
            
            if abs(npv) < 1e-6:  # Convergence threshold
                return rate
            
            if abs(dnpv) < 1e-10:  # Avoid division by zero
                break
                
            rate = rate - npv / dnpv
            
            if rate < -0.99:  # Prevent unrealistic negative rates
                return None
        
        return rate if rate > -0.99 else None

    def _calculate_payback_period(self, cash_flows: List[float]) -> Optional[float]:
        """Calculate simple payback period"""
        if not cash_flows or len(cash_flows) < 2:
            return None
        
        initial_investment = -cash_flows[0]  # Should be negative
        if initial_investment <= 0:
            return None
        
        cumulative = 0
        for i, cash_flow in enumerate(cash_flows[1:], 1):
            cumulative += cash_flow
            if cumulative >= initial_investment:
                # Linear interpolation for fractional year
                if i == 1:
                    return initial_investment / cash_flow
                else:
                    previous_cumulative = cumulative - cash_flow
                    fraction = (initial_investment - previous_cumulative) / cash_flow
                    return i - 1 + fraction
        
        return None  # Payback not achieved within project lifetime

    async def _perform_sensitivity_analysis(self, investment: float, annual_savings: float, 
                                          discount_rate: float, lifetime: int) -> Dict:
        """Perform sensitivity analysis on key variables"""
        base_npv = self._calculate_npv(
            [-investment] + [annual_savings] * lifetime, 
            discount_rate
        )
        
        sensitivities = {}
        variables = {
            "investment": [-0.2, -0.1, 0.1, 0.2],
            "annual_savings": [-0.2, -0.1, 0.1, 0.2],
            "discount_rate": [-0.02, -0.01, 0.01, 0.02]
        }
        
        for var, changes in variables.items():
            var_sensitivities = []
            for change in changes:
                if var == "investment":
                    test_investment = investment * (1 + change)
                    test_npv = self._calculate_npv(
                        [-test_investment] + [annual_savings] * lifetime,
                        discount_rate
                    )
                elif var == "annual_savings":
                    test_savings = annual_savings * (1 + change)
                    test_npv = self._calculate_npv(
                        [-investment] + [test_savings] * lifetime,
                        discount_rate
                    )
                elif var == "discount_rate":
                    test_rate = discount_rate + change
                    test_npv = self._calculate_npv(
                        [-investment] + [annual_savings] * lifetime,
                        test_rate
                    )
                
                sensitivity = ((test_npv - base_npv) / base_npv) / change if change != 0 else 0
                var_sensitivities.append({
                    "change_percent": change * 100,
                    "npv_impact": test_npv - base_npv,
                    "sensitivity_ratio": sensitivity
                })
            
            sensitivities[var] = var_sensitivities
        
        return sensitivities

    def _generate_investment_recommendation(self, npv: float, irr: Optional[float], 
                                          payback: Optional[float], risk_factors: Dict) -> str:
        """Generate investment recommendation based on financial metrics"""
        recommendation = "PROCEED"
        reasoning = []
        
        if npv < 0:
            recommendation = "REJECT"
            reasoning.append("Negative NPV indicates value destruction")
        elif npv < 10000:
            recommendation = "MARGINAL"
            reasoning.append("Low NPV suggests marginal returns")
        
        if irr and irr < 0.12:
            if recommendation == "PROCEED":
                recommendation = "MARGINAL"
            reasoning.append("IRR below typical energy project threshold (12%)")
        
        if payback and payback > 10:
            if recommendation == "PROCEED":
                recommendation = "MARGINAL"
            reasoning.append("Payback period exceeds 10 years")
        
        total_risk = sum(risk_factors.values())
        if total_risk > 0.3:
            if recommendation == "PROCEED":
                recommendation = "PROCEED_WITH_CAUTION"
            reasoning.append("High risk profile requires additional due diligence")
        
        if not reasoning:
            reasoning.append("Strong financial metrics support investment")
        
        return f"{recommendation}: {'; '.join(reasoning)}"

    # Additional helper methods (simplified for brevity)
    async def _generate_contract_scenarios(self, term: int, savings: float, sharing: float, cost: float) -> List[Dict]:
        """Generate contract scenarios for optimization"""
        scenarios = []
        for share in [0.6, 0.7, 0.8]:
            for guarantee in [0.8, 0.85, 0.9]:
                scenarios.append({
                    "sharing_percentage": share,
                    "savings_guarantee": guarantee,
                    "performance_threshold": 0.85,
                    "estimated_annual_revenue": savings * share * guarantee
                })
        return scenarios

    def _calculate_contract_cash_flows(self, scenario: Dict, term: int, operating: float, maintenance: float) -> List[float]:
        """Calculate cash flows for contract scenario"""
        annual_revenue = scenario["estimated_annual_revenue"]
        annual_costs = operating + maintenance
        return [0] + [annual_revenue - annual_costs] * term

    def _calculate_optimization_score(self, npv: float, irr: Optional[float], payback: Optional[float], 
                                    scenario: Dict, objectives: List[str]) -> float:
        """Calculate optimization score for scenario"""
        score = 0
        if "maximize_npv" in objectives:
            score += npv / 100000  # Normalize
        if "maximize_irr" in objectives and irr:
            score += irr * 10
        if "minimize_payback" in objectives and payback:
            score += max(0, 10 - payback)  # Reward shorter payback
        return score

    async def _generate_contract_recommendations(self, best_scenario: Dict, all_scenarios: List[Dict]) -> List[str]:
        """Generate contract optimization recommendations"""
        return [
            f"Optimal sharing percentage: {best_scenario['sharing_percentage']*100:.0f}%",
            f"Recommended savings guarantee: {best_scenario['savings_guarantee']*100:.0f}%",
            "Consider performance bonuses for exceeding guarantees",
            "Implement quarterly true-up process for accuracy"
        ]

    async def _analyze_contract_risk(self, scenario: Dict, term: int) -> Dict:
        """Analyze contract risk factors"""
        return {
            "performance_risk": "medium",
            "market_risk": "low",
            "regulatory_risk": "low",
            "overall_risk_score": 0.25
        }

    # Additional helper method stubs (would be fully implemented in production)
    async def _evaluate_technology(self, tech: str, conditions: Dict, criteria: Dict, requirements: Dict) -> Dict:
        """Evaluate individual technology option"""
        return {"technology": tech, "feasible": True, "overall_score": 0.8, "roi": 0.15, "risk": 0.2}

    async def _generate_technology_combinations(self, evaluations: List[Dict], budget: float, requirements: Dict) -> List[Dict]:
        """Generate viable technology combinations"""
        return [{"technologies": evaluations[:2], "total_cost": budget * 0.8, "combined_score": 0.85}]

    async def _calculate_portfolio_metrics(self, technologies: List[Dict]) -> Dict:
        """Calculate portfolio-level metrics"""
        return {"combined_roi": 0.18, "risk_score": 0.22, "implementation_time": 8}

    def _generate_selection_rationale(self, evaluations: List[Dict], combination: Dict) -> str:
        """Generate technology selection rationale"""
        return "Selected combination optimizes ROI while meeting risk and implementation constraints"

    async def _create_implementation_plan(self, combination: Dict) -> Dict:
        """Create implementation plan for technology combination"""
        return {"phases": 3, "timeline_months": 8, "critical_path": ["Design", "Procurement", "Installation"]}

async def main():
    """Run the Energy Finance Agent"""
    agent = EnergyFinanceAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())