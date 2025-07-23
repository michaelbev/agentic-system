"""Base planner for workflow orchestration."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BasePlanner(ABC):
    """Abstract base class for workflow planners."""
    
    @abstractmethod
    async def create_workflow(self, user_request: str, 
                            available_agents: List[str]) -> Dict[str, Any]:
        """Create a workflow plan from user request."""
        pass