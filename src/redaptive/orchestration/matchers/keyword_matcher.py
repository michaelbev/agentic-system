"""Keyword-based intent matcher."""

from typing import Dict, List, Any
from .base_matcher import BaseMatcher

class KeywordMatcher(BaseMatcher):
    """Matcher based on keyword recognition."""
    
    def __init__(self):
        self.keywords = {
            "energy": ["energy", "consumption", "usage", "kwh", "meter"],
            "portfolio": ["portfolio", "buildings", "facilities", "properties"],
            "finance": ["roi", "cost", "savings", "budget", "financial"],
            "monitoring": ["monitor", "alert", "anomaly", "real-time", "iot"]
        }
    
    async def match_intent(self, user_input: str) -> Dict[str, Any]:
        """Match user input to agent capabilities."""
        user_lower = user_input.lower()
        matches = {}
        
        for category, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_lower)
            if score > 0:
                matches[category] = score / len(keywords)
        
        # Find best match
        best_match = max(matches.items(), key=lambda x: x[1]) if matches else ("unknown", 0.0)
        
        return {
            "intent": best_match[0],
            "confidence": best_match[1],
            "all_matches": matches
        }