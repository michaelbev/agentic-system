#!/usr/bin/env python3
"""
Redaptive Agentic Platform - Main Entry Point
"""

import asyncio
import sys
import argparse
import logging
from redaptive.agents import AGENT_REGISTRY, get_agent

def main():
    parser = argparse.ArgumentParser(description="Redaptive Agentic AI Platform")
    parser.add_argument("agent", choices=list(AGENT_REGISTRY.keys()), 
                       help="Agent to start")
    parser.add_argument("--log-level", default="INFO", 
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=getattr(logging, args.log_level.upper()))
    
    # Get and start agent
    agent_class = get_agent(args.agent)
    if not agent_class:
        print(f"Agent not found: {args.agent}")
        sys.exit(1)
    
    agent = agent_class()
    
    print(f"🤖 Starting {args.agent} agent...")
    asyncio.run(agent.run())

if __name__ == "__main__":
    main()
