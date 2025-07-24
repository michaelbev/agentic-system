"""Hybrid planner that uses learning-based as primary with rule-based fallback."""

import asyncio
from typing import Dict, List, Any
from .base_planner import BasePlanner
from .llm_planner import LearningBasedPlanner
from .dynamic_planner import DynamicPlanner

class HybridPlanner(BasePlanner):
    """Hybrid planner that uses learning-based as primary with rule-based fallback."""
    
    def __init__(self, learning_primary: bool = True, fallback_threshold: float = 0.8):
        self.learning_primary = learning_primary
        self.fallback_threshold = fallback_threshold
        self.learning_planner = LearningBasedPlanner()
        self.rule_based_planner = DynamicPlanner()
    
    async def create_workflow(self, user_request: str, 
                            available_agents: List[str]) -> Dict[str, Any]:
        """Create workflow using learning-based with rule-based fallback."""
        
        if not self.learning_primary:
            # Use rule-based as primary
            result = await self.rule_based_planner.create_workflow(user_request, available_agents)
            result["planning_method"] = "rule_based"
            result["planning_reason"] = "Rule-based planner used as primary"
            return result
        
        try:
            # Try learning-based first
            learning_result = await self.learning_planner.create_workflow(user_request, available_agents)
            
            # Validate learning-based result
            if self._validate_learning_result(learning_result):
                learning_result["planning_method"] = "learning_based"
                learning_result["planning_reason"] = "Learning-based planner used successfully"
                return learning_result
            else:
                # Learning-based result is invalid, fallback to rule-based
                print(f"⚠️ Learning-based result invalid, falling back to rule-based planner")
                result = await self.rule_based_planner.create_workflow(user_request, available_agents)
                result["planning_method"] = "rule_based"
                result["planning_reason"] = "Learning-based result invalid, fallback to rule-based"
                return result
                
        except Exception as e:
            # Learning-based failed, fallback to rule-based
            print(f"⚠️ Learning-based planner failed: {e}, falling back to rule-based planner")
            result = await self.rule_based_planner.create_workflow(user_request, available_agents)
            result["planning_method"] = "rule_based"
            result["planning_reason"] = f"Learning-based failed ({str(e)}), fallback to rule-based"
            return result
    
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
    
    async def get_planner_stats(self) -> Dict[str, Any]:
        """Get statistics about planner usage."""
        return {
            "primary_method": "learning_based" if self.learning_primary else "rule_based",
            "fallback_threshold": self.fallback_threshold,
            "available_planners": ["learning_based", "rule_based", "hybrid"]
        } 