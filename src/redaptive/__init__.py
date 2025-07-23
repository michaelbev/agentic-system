"""
Redaptive Agentic AI Platform
============================

A multi-agent AI system for Energy-as-a-Service (EaaS) portfolio management and optimization.
"""

__version__ = "0.3.0"
__author__ = "Redaptive AI Team"

from .config import settings
from .agents import AGENT_REGISTRY

__all__ = ["settings", "AGENT_REGISTRY", "__version__"]