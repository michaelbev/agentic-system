"""Base matcher for intent recognition."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseMatcher(ABC):
    """Abstract base class for intent matchers."""
    
    @abstractmethod
    async def match_intent(self, user_input: str) -> Dict[str, Any]:
        """Match user input to agent capabilities."""
        pass