#!/usr/bin/env python3
"""
System Agent for handling system-level operations like scope checking
"""

import json
from datetime import datetime
import pytz
from redaptive.agents.base import BaseMCPServer

class SystemAgent(BaseMCPServer):
    """System agent for handling system-level operations."""
    
    def __init__(self):
        super().__init__("system-agent", "1.0.0")
        self.setup_tools()
        
    def setup_tools(self):
        """Setup system tools."""
        self.register_tool(
            "scope_check",
            "Check if a request is within system scope",
            self.scope_check,
            {
                "type": "object",
                "properties": {
                    "scope": {"type": "string"},
                    "system_domain": {"type": "string"},
                    "supported_topics": {"type": "array", "items": {"type": "string"}},
                    "unsupported_topics": {"type": "array", "items": {"type": "string"}},
                    "recommendation": {"type": "string"}
                }
            }
        )
        
        self.register_tool(
            "get_current_time",
            "Get current time in specified timezone",
            self.get_current_time,
            {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "default": "America/Denver"}
                }
            }
        )
    
    async def scope_check(self, scope: str, system_domain: str, 
                         supported_topics: list, unsupported_topics: list, 
                         recommendation: str) -> dict:
        """Check if a request is within system scope."""
        return {
            "scope": scope,
            "system_domain": system_domain,
            "supported_topics": supported_topics,
            "unsupported_topics": unsupported_topics,
            "recommendation": recommendation,
            "analysis": "This request is outside the scope of the Redaptive Energy-as-a-Service platform."
        }
    
    async def get_current_time(self, timezone: str = "America/Denver") -> dict:
        """Get current time in specified timezone."""
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        
        return {
            "current_date": now.strftime("%Y-%m-%d"),
            "current_time": now.strftime("%H:%M:%S"),
            "timezone": timezone,
            "full_datetime": now.isoformat(),
            "day_of_week": now.strftime("%A"),
            "analysis": f"Current date: {now.strftime('%A, %B %d, %Y')} at {now.strftime('%I:%M %p')} {now.tzname()}"
        }

if __name__ == "__main__":
    import asyncio
    agent = SystemAgent()
    asyncio.run(agent.run()) 