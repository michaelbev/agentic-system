"""Configuration for workflow planners."""

from enum import Enum
from typing import Dict, Any

class PlannerType(Enum):
    """Available planner types."""
    RULE_BASED = "rule_based"
    LEARNING_BASED = "learning_based"
    HYBRID = "hybrid"

class PlannerConfig:
    """Configuration for workflow planners."""
    
    def __init__(self, planner_type: str = "hybrid"):
        self.planner_type = PlannerType(planner_type)
        self.config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "planner_type": self.planner_type.value,
            "learning_primary": True,
            "fallback_threshold": 0.8,
            "enable_validation": True,
            "enable_logging": True,
            "timeout_seconds": 30,
            "max_retries": 3
        }
    
    def get_planner_class(self):
        """Get the appropriate planner class based on configuration."""
        from redaptive.orchestration.planners import DynamicPlanner, LearningBasedPlanner, HybridPlanner
        
        if self.planner_type == PlannerType.RULE_BASED:
            return DynamicPlanner
        elif self.planner_type == PlannerType.LEARNING_BASED:
            return LearningBasedPlanner
        elif self.planner_type == PlannerType.HYBRID:
            return HybridPlanner
        else:
            raise ValueError(f"Unknown planner type: {self.planner_type}")
    
    def get_planner_kwargs(self) -> Dict[str, Any]:
        """Get keyword arguments for planner initialization."""
        if self.planner_type == PlannerType.HYBRID:
            return {
                "learning_primary": self.config["learning_primary"],
                "fallback_threshold": self.config["fallback_threshold"]
            }
        return {}
    
    def update_config(self, **kwargs):
        """Update configuration."""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value 