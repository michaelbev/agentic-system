"""Keyword-based intent matcher."""

from typing import Dict, List, Any
from .base_matcher import BaseMatcher

class KeywordMatcher(BaseMatcher):
    """Matcher based on keyword recognition."""
    
    def __init__(self):
        self.keywords = {
            "energy": ["energy", "consumption", "usage", "kwh", "meter", "electricity", "power", "demand", "reading", "data", "monitor", "sensor"],
            "portfolio": ["portfolio", "buildings", "facilities", "properties", "sites", "locations", "performance", "metrics", "benchmark", "sustainability"],
            "finance": ["roi", "cost", "savings", "budget", "financial", "investment", "payback", "revenue"],
            "monitoring": ["monitor", "alert", "anomaly", "real-time", "iot", "sensor", "data", "reading", "latest", "recent"],
            "document": ["document", "pdf", "report", "summarize", "extract", "text", "file"],
            "time": ["date", "time", "current", "now", "today", "what time", "what date"]
        }
        
        # Out-of-scope keywords that should be rejected
        self.out_of_scope_keywords = [
            "president", "history", "politics", "government", "election", "congress", "senate", "house",
            "democrat", "republican", "biden", "trump", "obama", "bush", "clinton", "reagan", "carter",
            "weather", "forecast", "temperature", "rain", "snow", "sunny", "cloudy", "humidity",
            "sports", "football", "basketball", "baseball", "soccer", "tennis", "golf", "hockey",
            "recipe", "cook", "bake", "food", "kitchen", "cake", "chocolate",
            "capital", "country", "geography", "map", "location", "france", "rome"
        ]
    
    async def match_intent(self, user_input: str) -> Dict[str, Any]:
        """Match user input to agent capabilities."""
        user_lower = user_input.lower()
        
        # First check for out-of-scope keywords
        for keyword in self.out_of_scope_keywords:
            if keyword in user_lower:
                return {
                    "intent": "out_of_scope",
                    "confidence": 1.0,
                    "reason": f"Contains out-of-scope keyword: {keyword}",
                    "all_matches": {"out_of_scope": 1.0}
                }
        
        # Special handling for energy-specific date queries
        if any(word in user_lower for word in ["energy", "consumption", "usage", "meter", "reading", "data"]) and any(word in user_lower for word in ["date", "time", "when", "latest", "recent", "most recent"]):
            return {
                "intent": "energy_monitoring",
                "confidence": 0.95,
                "reason": "Energy-specific date/time query detected",
                "all_matches": {"energy_monitoring": 0.95, "time": 0.3}
            }
        
        # Then check for in-scope keywords
        matches = {}
        for category, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_lower)
            if score > 0:
                matches[category] = score / len(keywords)
        
        # Find best match
        if matches:
            best_match = max(matches.items(), key=lambda x: x[1])
            return {
                "intent": best_match[0],
                "confidence": best_match[1],
                "all_matches": matches
            }
        else:
            # No clear intent found
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "all_matches": {}
            }