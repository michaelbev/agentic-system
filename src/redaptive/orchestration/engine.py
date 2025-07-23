"""
Main orchestration engine for coordinating multiple agents.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from redaptive.agents import AGENT_REGISTRY, get_agent
from redaptive.config import settings

logger = logging.getLogger(__name__)

class OrchestrationEngine:
    """Main engine for coordinating multiple agents in workflows."""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.running_workflows: Dict[str, Dict[str, Any]] = {}
        self.max_concurrent = settings.agents.max_concurrent_agents
        
    async def initialize_agents(self, agent_names: List[str]) -> bool:
        """Initialize specified agents."""
        try:
            for agent_name in agent_names:
                if agent_name in AGENT_REGISTRY:
                    agent_class = get_agent(agent_name)
                    self.agents[agent_name] = agent_class()
                    logger.info(f"Initialized agent: {agent_name}")
                else:
                    logger.warning(f"Unknown agent: {agent_name}")
            
            return len(self.agents) > 0
        except Exception as e:
            logger.error(f"Failed to initialize agents: {e}")
            return False
    
    async def execute_workflow(self, workflow_id: str, 
                             workflow_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a multi-agent workflow."""
        try:
            self.running_workflows[workflow_id] = {
                "status": "running",
                "started_at": "2024-01-01T00:00:00Z",
                "steps_completed": 0,
                "total_steps": len(workflow_definition.get("steps", []))
            }
            
            results = {}
            steps = workflow_definition.get("steps", [])
            
            for i, step in enumerate(steps):
                agent_name = step.get("agent")
                tool_name = step.get("tool")
                parameters = step.get("parameters", {})
                
                if agent_name not in self.agents:
                    raise ValueError(f"Agent not initialized: {agent_name}")
                
                # Execute the tool on the agent
                agent = self.agents[agent_name]
                if tool_name not in agent.tools:
                    raise ValueError(f"Tool not found: {tool_name} on agent {agent_name}")
                
                tool = agent.tools[tool_name]
                if asyncio.iscoroutinefunction(tool.handler):
                    result = await tool.handler(**parameters)
                else:
                    result = tool.handler(**parameters)
                
                results[f"step_{i+1}"] = {
                    "agent": agent_name,
                    "tool": tool_name,
                    "result": result
                }
                
                self.running_workflows[workflow_id]["steps_completed"] = i + 1
                logger.info(f"Completed workflow step {i+1}/{len(steps)}")
            
            self.running_workflows[workflow_id]["status"] = "completed"
            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            self.running_workflows[workflow_id]["status"] = "failed"
            return {
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e)
            }
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the status of a running workflow."""
        return self.running_workflows.get(workflow_id, {"status": "not_found"})
    
    async def list_available_agents(self) -> List[Dict[str, Any]]:
        """List all available agents and their tools."""
        agent_list = []
        for agent_name, agent_instance in self.agents.items():
            tools = [
                {
                    "name": tool.name,
                    "description": tool.description
                }
                for tool in agent_instance.tools.values()
            ]
            
            agent_list.append({
                "name": agent_name,
                "status": "initialized",
                "tools": tools
            })
        
        return agent_list
    
    async def shutdown(self):
        """Shutdown all agents and cleanup resources."""
        for agent_name, agent in self.agents.items():
            try:
                if hasattr(agent, 'disconnect'):
                    agent.disconnect()
                logger.info(f"Shutdown agent: {agent_name}")
            except Exception as e:
                logger.error(f"Error shutting down agent {agent_name}: {e}")
        
        self.agents.clear()
        self.running_workflows.clear()