"""
Redaptive Agent Registry
=======================

Central registry for all agents in the Redaptive Agentic AI Platform.
"""

from .energy import (
    PortfolioIntelligenceAgent,
    EnergyMonitoringAgent,
    EnergyFinanceAgent
)
from .content import (
    DocumentProcessingAgent,
    SummarizeAgent
)

# Agent registry for discovery and orchestration
AGENT_REGISTRY = {
    # Energy domain agents
    'portfolio-intelligence': PortfolioIntelligenceAgent,
    'energy-monitoring': EnergyMonitoringAgent,
    'energy-finance': EnergyFinanceAgent,
    
    # Content processing agents  
    'document-processing': DocumentProcessingAgent,
    'summarize': SummarizeAgent,
}

__all__ = [
    "AGENT_REGISTRY",
    "PortfolioIntelligenceAgent",
    "EnergyMonitoringAgent", 
    "EnergyFinanceAgent",
    "DocumentProcessingAgent",
    "SummarizeAgent"
]

def get_agent(agent_name: str):
    """Get an agent class by name."""
    return AGENT_REGISTRY.get(agent_name)

def list_agents():
    """List all available agents."""
    return list(AGENT_REGISTRY.keys())

def get_agents_by_domain(domain: str):
    """Get agents by domain (energy, content)."""
    if domain == "energy":
        return {
            k: v for k, v in AGENT_REGISTRY.items() 
            if k in ['portfolio-intelligence', 'energy-monitoring', 'energy-finance']
        }
    elif domain == "content":
        return {
            k: v for k, v in AGENT_REGISTRY.items()
            if k in ['document-processing', 'summarize']
        }
    else:
        return {}