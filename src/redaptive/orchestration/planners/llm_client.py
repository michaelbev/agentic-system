"""LLM client interface for workflow planning."""

import asyncio
from typing import Optional, Dict, Any
import os

# Optional OpenAI import
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Optional Anthropic import
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

class LLMClient:
    """Generic LLM client interface for learning-based planning."""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.provider = provider
        
        # Set API key based on provider
        if provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        elif provider == "anthropic":
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        else:
            self.api_key = api_key
        
        # Validate credentials
        self._validate_credentials()
        
        # Initialize provider-specific clients
        if provider == "openai" and self.api_key and OPENAI_AVAILABLE:
            openai.api_key = self.api_key
        elif provider == "anthropic" and self.api_key and ANTHROPIC_AVAILABLE:
            self.anthropic_client = anthropic.Anthropic(api_key=self.api_key)
    
    def _validate_credentials(self):
        """Validate that credentials are properly configured."""
        if self.provider == "openai":
            if not self.api_key:
                print("⚠️  OPENAI_API_KEY not found in environment variables.")
                print("   The system will use rule-based planning instead of learning-based planning.")
                print("   To enable learning-based planning, set OPENAI_API_KEY in your .env file:")
                print("   OPENAI_API_KEY=your_openai_api_key_here")
            elif not OPENAI_AVAILABLE:
                print("⚠️  OpenAI package not installed. Install with: pip install openai")
                print("   The system will use rule-based planning instead of learning-based planning.")
            else:
                print("✅ OpenAI credentials configured for learning-based planning")
        elif self.provider == "anthropic":
            if not self.api_key:
                print("⚠️  ANTHROPIC_API_KEY not found in environment variables.")
                print("   The system will use rule-based planning instead of learning-based planning.")
                print("   To enable learning-based planning, set ANTHROPIC_API_KEY in your .env file:")
                print("   ANTHROPIC_API_KEY=your_anthropic_api_key_here")
            elif not ANTHROPIC_AVAILABLE:
                print("⚠️  Anthropic package not installed. Install with: pip install anthropic")
                print("   The system will use rule-based planning instead of learning-based planning.")
            else:
                print("✅ Anthropic/Claude credentials configured for learning-based planning")
    
    async def generate(self, prompt: str, model: str = None) -> str:
        """Generate response from LLM."""
        if self.provider == "openai" and self.api_key and OPENAI_AVAILABLE:
            return await self._generate_openai(prompt, model or "gpt-3.5-turbo")
        elif self.provider == "anthropic" and self.api_key and ANTHROPIC_AVAILABLE:
            return await self._generate_anthropic(prompt, model or "claude-3-5-sonnet-20241022")
        else:
            # Fallback to mock response for testing
            return await self._generate_mock(prompt)
    
    async def _generate_openai(self, prompt: str, model: str) -> str:
        """Generate response using OpenAI API."""
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an intelligent workflow planner. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent planning
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return await self._generate_mock(prompt)
    
    async def _generate_anthropic(self, prompt: str, model: str) -> str:
        """Generate response using Anthropic/Claude API."""
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                temperature=0.1,  # Low temperature for consistent planning
                system="You are an intelligent workflow planner. Always respond with valid JSON.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return await self._generate_mock(prompt)
    
    async def _generate_mock(self, prompt: str) -> str:
        """Generate mock response for testing without API key."""
        # More intelligent keyword-based mock responses
        prompt_lower = prompt.lower()
        
        # Energy-specific date/time queries
        if any(word in prompt_lower for word in ["energy", "meter", "reading", "data"]) and any(word in prompt_lower for word in ["date", "latest", "recent", "most recent"]):
            return '''{
                "workflow_id": "energy_monitoring_date_workflow",
                "reasoning": "User is asking for latest energy reading date, should query the energy monitoring database",
                "steps": [
                    {
                        "agent": "energy-monitoring",
                        "tool": "get_latest_energy_reading",
                        "parameters": {"include_details": true},
                        "reasoning": "Query the database for the most recent energy reading"
                    }
                ]
            }'''
        
        # General time/date queries (not energy-specific)
        elif any(word in prompt_lower for word in ["time", "date", "current", "now"]) and not any(word in prompt_lower for word in ["energy", "meter", "reading"]):
            return '''{
                "workflow_id": "time_analysis_workflow", 
                "reasoning": "User is asking for current time/date",
                "steps": [
                    {
                        "agent": "system",
                        "tool": "get_current_time", 
                        "parameters": {"timezone": "America/Denver"},
                        "reasoning": "Get current system time"
                    }
                ]
            }'''
        
        # Financial/ROI queries
        elif any(word in prompt_lower for word in ["roi", "financial", "cost", "investment", "calculate"]):
            return '''{
                "workflow_id": "financial_analysis_workflow",
                "reasoning": "User is asking for financial analysis or ROI calculation",
                "steps": [
                    {
                        "agent": "energy-finance",
                        "tool": "calculate_project_roi",
                        "parameters": {"project_details": {"type": "LED", "cost": 50000}},
                        "reasoning": "Calculate ROI for energy efficiency project"
                    }
                ]
            }'''
        
        # Energy optimization queries
        elif any(word in prompt_lower for word in ["optimization", "opportunities", "efficiency", "savings"]):
            return '''{
                "workflow_id": "energy_optimization_workflow",
                "reasoning": "User is asking for energy optimization opportunities",
                "steps": [
                    {
                        "agent": "portfolio-intelligence",
                        "tool": "identify_optimization_opportunities",
                        "parameters": {"buildings_list": ["building_123"], "opportunity_types": ["LED", "HVAC"]},
                        "reasoning": "Find energy optimization opportunities across portfolio"
                    }
                ]
            }'''
        
        # Out-of-scope queries
        elif any(word in prompt_lower for word in ["president", "history", "weather", "recipe", "sports"]):
            return '''{
                "workflow_id": "out_of_scope_workflow",
                "reasoning": "Request is outside the system's scope",
                "steps": [
                    {
                        "agent": "system",
                        "tool": "scope_check",
                        "parameters": {"scope": "out_of_bounds"},
                        "reasoning": "Check if request is within system scope"
                    }
                ]
            }'''
        
        # General energy analysis
        elif any(word in prompt_lower for word in ["energy", "consumption", "usage", "analyze"]):
            return '''{
                "workflow_id": "energy_analysis_workflow",
                "reasoning": "User is asking for energy analysis",
                "steps": [
                    {
                        "agent": "energy-monitoring",
                        "tool": "analyze_usage_patterns",
                        "parameters": {"scope": "building", "identifier": "building_123"},
                        "reasoning": "Analyze energy usage patterns"
                    }
                ]
            }'''
        
        # Default fallback
        else:
            return '''{
                "workflow_id": "general_analysis_workflow",
                "reasoning": "General analysis request",
                "steps": [
                    {
                        "agent": "system", 
                        "tool": "scope_check",
                        "parameters": {"scope": "general"},
                        "reasoning": "Check if request is within system scope"
                    }
                ]
            }''' 