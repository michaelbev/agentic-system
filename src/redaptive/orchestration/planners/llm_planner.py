"""LLM-based workflow planner using natural language understanding."""

import json
import asyncio
import os
from typing import Dict, List, Any, Optional
from .base_planner import BasePlanner

class LearningBasedPlanner(BasePlanner):
    """Modern learning-based planner that uses natural language understanding."""
    
    def __init__(self, learning_client=None):
        self.learning_client = learning_client or self._get_default_learning()
    
    def _get_default_learning(self):
        """Get default learning-based client."""
        from .llm_client import LLMClient
        
        # Check for preferred provider
        preferred_provider = os.getenv("PREFERRED_LLM_PROVIDER", "openai")
        
        if preferred_provider == "anthropic":
            return LLMClient(provider="anthropic")
        else:
            return LLMClient(provider="openai")
    
    def _get_tools_description(self, available_agents: List[str]) -> str:
        """Generate a description of available tools for the LLM."""
        tools_info = {
            "energy-monitoring": {
                "tools": {
                    "get_latest_energy_reading": "Get the most recent energy usage reading from database",
                    "process_meter_data": "Process real-time meter data with anomaly detection",
                    "analyze_usage_patterns": "Analyze energy consumption patterns for buildings"
                }
            },
            "energy-finance": {
                "tools": {
                    "calculate_project_roi": "Calculate ROI for energy efficiency projects",
                    "optimize_eaas_contract": "Optimize Energy-as-a-Service contract terms"
                }
            },
            "portfolio-intelligence": {
                "tools": {
                    "identify_optimization_opportunities": "Find energy optimization opportunities across portfolio",
                    "search_facilities": "Search for facilities matching criteria",
                    "analyze_portfolio_energy_usage": "Analyze energy usage across portfolio"
                }
            },
            "document-processing": {
                "tools": {
                    "extract_text": "Extract text from PDF documents",
                    "summarize_document": "Create summaries of documents"
                }
            },
            "system": {
                "tools": {
                    "get_current_time": "Get current date and time",
                    "scope_check": "Check if request is within system scope"
                }
            }
        }
        
        description = "Available agents and their tools:\n"
        for agent in available_agents:
            if agent in tools_info:
                description += f"\n{agent}:\n"
                for tool, desc in tools_info[agent]["tools"].items():
                    description += f"  - {tool}: {desc}\n"
        
        return description
    
    async def create_workflow(self, user_request: str, 
                            available_agents: List[str]) -> Dict[str, Any]:
        """Create a workflow plan using learning-based reasoning."""
        
        if not self.learning_client:
            # Fallback to rule-based planning if no learning-based available
            return await self._fallback_planning(user_request, available_agents)
        
        try:
            # Use the user request directly - the learning client handles the logic
            response = await self.learning_client.generate(user_request)
            
            # Parse JSON response
            try:
                workflow_plan = json.loads(response)
                workflow_plan["planning_method"] = "learning_based"
                workflow_plan["planning_reason"] = "Learning-based generated workflow plan"
                return workflow_plan
            except json.JSONDecodeError:
                # Fallback if learning-based doesn't return valid JSON
                return await self._fallback_planning(user_request, available_agents)
                
        except Exception as e:
            # Fallback on any error
            return await self._fallback_planning(user_request, available_agents)
    
    async def _fallback_planning(self, user_request: str, 
                                available_agents: List[str]) -> Dict[str, Any]:
        """Fallback to rule-based planning when learning-based is unavailable."""
        from .dynamic_planner import DynamicPlanner
        
        fallback_planner = DynamicPlanner()
        return await fallback_planner.create_workflow(user_request, available_agents) 