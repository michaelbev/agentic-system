"""Adaptive planner that can switch between systematic and learning-based planning."""

import asyncio
import re
from typing import Dict, List, Any, Optional
from .base_planner import BasePlanner
from .llm_planner import LearningBasedPlanner
from .dynamic_planner import DynamicPlanner
from .hybrid_planner import HybridPlanner

class AdaptivePlanner(BasePlanner):
    """Adaptive planner that can switch between systematic and learning-based planning."""
    
    def __init__(self, default_method: str = "systematic"):
        """
        Initialize adaptive planner.
        
        Args:
            default_method: Default planning method ("systematic", "learning", "hybrid", "auto")
        """
        super().__init__()
        self.default_method = default_method
        self.systematic_planner = DynamicPlanner()
        self.learning_planner = LearningBasedPlanner()
        self.hybrid_planner = HybridPlanner(learning_primary=True)
        
        # Planning method keywords for automatic detection
        self.method_keywords = {
            "systematic": ["systematic", "rule-based", "rules", "structured", "deterministic"],
            "learning": ["learning", "ai", "intelligent", "smart", "adaptive", "dynamic"],
            "hybrid": ["hybrid", "combined", "both", "mixed", "flexible"],
            "auto": ["auto", "automatic", "best", "optimal", "smart"]
        }
    
    async def create_workflow(self, user_request: str, 
                            available_agents: List[str],
                            planning_method: Optional[str] = None) -> Dict[str, Any]:
        """
        Create workflow using specified or detected planning method.
        
        Args:
            user_request: The user's request
            available_agents: List of available agents
            planning_method: Explicit planning method ("systematic", "learning", "hybrid", "auto")
        """
        
        # Determine planning method
        method = self._determine_planning_method(user_request, planning_method)
        
        print(f"🎯 Using planning method: {method}")
        
        # Execute planning based on method
        if method == "systematic":
            return await self._create_systematic_workflow(user_request, available_agents)
        elif method == "learning":
            return await self._create_learning_workflow(user_request, available_agents)
        elif method == "hybrid":
            return await self._create_hybrid_workflow(user_request, available_agents)
        elif method == "auto":
            return await self._create_auto_workflow(user_request, available_agents)
        else:
            # Fallback to systematic
            return await self._create_systematic_workflow(user_request, available_agents)
    
    def _determine_planning_method(self, user_request: str, explicit_method: Optional[str] = None) -> str:
        """Determine which planning method to use."""
        
        # If explicit method provided, use it
        if explicit_method:
            if explicit_method in ["systematic", "learning", "hybrid", "auto"]:
                return explicit_method
            else:
                print(f"⚠️ Invalid planning method '{explicit_method}', using default")
        
        # Check for method keywords in user request
        user_lower = user_request.lower()
        
        for method, keywords in self.method_keywords.items():
            for keyword in keywords:
                if keyword in user_lower:
                    print(f"🎯 Detected planning method '{method}' from keyword '{keyword}'")
                    return method
        
        # Check for special patterns
        if re.search(r'use\s+(systematic|rule-based|learning|ai|hybrid)', user_lower):
            match = re.search(r'use\s+(systematic|rule-based|learning|ai|hybrid)', user_lower)
            method = match.group(1)
            if method in ["rule-based"]:
                method = "systematic"
            elif method in ["ai"]:
                method = "learning"
            print(f"🎯 Detected planning method '{method}' from 'use' pattern")
            return method
        
        # Use default method
        print(f"🎯 Using default planning method: {self.default_method}")
        return self.default_method
    
    async def _create_systematic_workflow(self, user_request: str, available_agents: List[str]) -> Dict[str, Any]:
        """Create workflow using systematic (rule-based) planning."""
        try:
            result = await self.systematic_planner.create_workflow(user_request, available_agents)
            result["planning_method"] = "systematic"
            result["planning_reason"] = f"Systematic planning used. {result.get('planning_reason', '')}"
            return result
        except Exception as e:
            return {
                "workflow_id": "systematic_planning_error",
                "planning_method": "systematic",
                "planning_reason": f"Systematic planning failed: {str(e)}",
                "error": str(e),
                "steps": []
            }
    
    async def _create_learning_workflow(self, user_request: str, available_agents: List[str]) -> Dict[str, Any]:
        """Create workflow using learning-based planning."""
        try:
            result = await self.learning_planner.create_workflow(user_request, available_agents)
            result["planning_method"] = "learning_based"
            result["planning_reason"] = f"Learning-based planning used. {result.get('planning_reason', '')}"
            return result
        except Exception as e:
            print(f"⚠️ Learning-based planning failed: {e}, falling back to systematic")
            return await self._create_systematic_workflow(user_request, available_agents)
    
    async def _create_hybrid_workflow(self, user_request: str, available_agents: List[str]) -> Dict[str, Any]:
        """Create workflow using hybrid planning."""
        try:
            result = await self.hybrid_planner.create_workflow(user_request, available_agents)
            result["planning_method"] = "hybrid"
            result["planning_reason"] = f"Hybrid planning used. {result.get('planning_reason', '')}"
            return result
        except Exception as e:
            print(f"⚠️ Hybrid planning failed: {e}, falling back to systematic")
            return await self._create_systematic_workflow(user_request, available_agents)
    
    async def _create_auto_workflow(self, user_request: str, available_agents: List[str]) -> Dict[str, Any]:
        """Create workflow using automatic method selection."""
        
        # Try learning-based first
        try:
            learning_result = await self.learning_planner.create_workflow(user_request, available_agents)
            if self._validate_learning_result(learning_result):
                learning_result["planning_method"] = "auto_learning"
                learning_result["planning_reason"] = f"Auto-selected learning-based planning. {learning_result.get('planning_reason', '')}"
                return learning_result
        except Exception as e:
            print(f"⚠️ Auto learning-based failed: {e}")
        
        # Fallback to systematic
        systematic_result = await self.systematic_planner.create_workflow(user_request, available_agents)
        systematic_result["planning_method"] = "auto_systematic"
        systematic_result["planning_reason"] = f"Auto-selected systematic planning (learning failed). {systematic_result.get('planning_reason', '')}"
        return systematic_result
    
    def _validate_learning_result(self, result: Dict[str, Any]) -> bool:
        """Validate that learning-based result has required structure."""
        try:
            # Check required fields
            if not result.get("workflow_id"):
                return False
            
            if not result.get("steps") or not isinstance(result["steps"], list):
                return False
            
            # Check each step has required fields
            for step in result["steps"]:
                if not step.get("agent") or not step.get("tool"):
                    return False
            
            return True
            
        except Exception:
            return False
    
    async def get_available_methods(self) -> Dict[str, Any]:
        """Get information about available planning methods."""
        return {
            "available_methods": ["systematic", "learning", "hybrid", "auto"],
            "default_method": self.default_method,
            "method_keywords": self.method_keywords,
            "descriptions": {
                "systematic": "Rule-based planning using predefined patterns and keyword matching",
                "learning": "AI-powered planning using LLM for dynamic workflow creation",
                "hybrid": "Combines learning-based with systematic fallback",
                "auto": "Automatically selects best method based on request complexity"
            }
        } 