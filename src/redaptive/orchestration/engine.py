"""
Main orchestration engine for coordinating multiple agents.
"""

import asyncio
import logging
import re
import json
from typing import Dict, List, Any, Optional
from redaptive.agents import AGENT_REGISTRY, get_agent
from redaptive.config import settings

logger = logging.getLogger(__name__)


class WorkflowStep:
    """Represents a single step in a workflow."""
    
    def __init__(self, agent_name: str, tool_name: str, arguments: Dict[str, Any]):
        self.agent_name = agent_name
        self.tool_name = tool_name
        self.arguments = arguments

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
    
    @property
    def workflow_patterns(self) -> Dict[str, Any]:
        """Return predefined workflow patterns for common tasks."""
        return {
            "summarize_pdf": {
                "goal": "summarize PDF content",
                "keywords": ["pdf", "summarize", "document"],
                "steps": [
                    {"agent": "textract", "tool": "extract_text"},
                    {"agent": "summarize", "tool": "summarize_text"}
                ]
            },
            "analyze_document": {
                "goal": "analyze document content and sentiment", 
                "keywords": ["analyze", "sentiment", "document"],
                "steps": [
                    {"agent": "textract", "tool": "extract_text"},
                    {"agent": "summarize", "tool": "analyze_sentiment"}
                ]
            },
            "extract_tables": {
                "goal": "extract tables from documents",
                "keywords": ["extract", "tables", "table"],
                "steps": [
                    {"agent": "textract", "tool": "extract_tables"}
                ]
            },
            "energy_data_analysis": {
                "description": "Analyze energy data",
                "keywords": ["energy", "analyze", "consumption", "building"],
                "tools": ["energy.analyze_consumption"],
                "steps": [
                    {"agent": "energy-monitoring", "tool": "get_facility_energy_data"}
                ]
            },
            "document_analysis": {
                "goal": "complete document analysis",
                "keywords": ["document", "analysis", "full"],
                "steps": [
                    {"agent": "textract", "tool": "extract_text"},
                    {"agent": "summarize", "tool": "summarize_text"},
                    {"agent": "summarize", "tool": "analyze_sentiment"}
                ]
            }
        }
    
    def _extract_keywords(self, user_request: str) -> List[str]:
        """Extract relevant keywords from user request for pattern matching."""
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', user_request.lower())
        
        # Define relevant keywords for different domains
        relevant_keywords = {
            "pdf", "document", "text", "file", "doc",
            "summarize", "summary", "analyze", "analysis", "extract", "process",
            "sentiment", "tables", "table", "data", "content",
            "energy", "consumption", "building", "facility", "power",
            "monitor", "performance", "efficiency", "usage"
        }
        
        # Return keywords that are in our relevant set
        return [word for word in words if word in relevant_keywords]
    
    def plan_workflow(self, user_request: str, context: Dict[str, Any]) -> List[WorkflowStep]:
        """Plan a workflow based on user request and context."""
        keywords = self._extract_keywords(user_request)
        
        # Find best matching pattern
        best_match = None
        best_score = 0
        
        for pattern_name, pattern in self.workflow_patterns.items():
            pattern_keywords = pattern.get("keywords", [])
            score = len(set(keywords) & set(pattern_keywords))
            if score > best_score:
                best_score = score
                best_match = pattern
        
        if not best_match or best_score == 0:
            # Fallback for unknown requests
            if "energy" in keywords or "building" in keywords:
                best_match = self.workflow_patterns["energy_data_analysis"]
            elif "document" in keywords or "pdf" in keywords:
                if "summarize" in keywords:
                    best_match = self.workflow_patterns["summarize_pdf"]
                else:
                    best_match = self.workflow_patterns["analyze_document"]
            else:
                # Default fallback
                return []
        
        # Convert pattern steps to WorkflowStep objects
        steps = []
        for step_def in best_match.get("steps", []):
            # Add context parameters
            arguments = dict(context)
            if step_def.get("agent") == "energy-monitoring" and "building" in user_request:
                # Extract building number if present
                building_match = re.search(r'building\s+(\d+)', user_request.lower())
                if building_match:
                    arguments["building_id"] = f"building_{building_match.group(1)}"
                else:
                    arguments["building_id"] = "building_123"  # Default fallback
            
            steps.append(WorkflowStep(
                agent_name=step_def["agent"],
                tool_name=step_def["tool"],
                arguments=arguments
            ))
        
        return steps
    
    def _resolve_arguments(self, arguments: Dict[str, Any], results: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve argument placeholders with values from previous steps."""
        resolved = {}
        
        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                # Extract placeholder like "{{step_0.full_text}}"
                placeholder = value[2:-2]
                if "." in placeholder:
                    step_ref, field = placeholder.split(".", 1)
                    if step_ref in results:
                        step_result = results[step_ref].get("result", {})
                        if "content" in step_result and step_result["content"]:
                            content = step_result["content"][0].get("text", "")
                            try:
                                data = json.loads(content)
                                resolved[key] = data.get(field, value)
                            except:
                                resolved[key] = content
                        else:
                            resolved[key] = value
                    else:
                        resolved[key] = value
                else:
                    resolved[key] = value
            else:
                resolved[key] = value
        
        return resolved
    
    def _generate_workflow_summary(self, workflow_steps: List[WorkflowStep], results: Dict[str, Any]) -> str:
        """Generate a human-readable summary of workflow execution."""
        if not workflow_steps:
            return "No workflow steps executed"
        
        step_count = len(workflow_steps)
        result_count = len([r for r in results.values() if r.get("result", {}).get("content")])
        
        # Try to determine what was accomplished
        agents_used = set(step.agent_name for step in workflow_steps)
        if "energy-monitoring" in agents_used:
            return f"Executed energy analysis workflow with {step_count} steps: Generated {result_count} energy analysis results"
        elif "textract" in agents_used:
            if "summarize" in agents_used:
                return f"Executed document analysis workflow with {step_count} steps: Generated {result_count} document processing results"
            else:
                return f"Executed text extraction workflow with {step_count} steps: Generated {result_count} extraction results"
        else:
            return f"Executed workflow with {step_count} steps: Generated {result_count} results"
    
    async def call_agent_tool(self, agent_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool on an agent with given arguments."""
        try:
            if agent_name not in self.agents:
                raise ValueError(f"Agent not initialized: {agent_name}")
            
            agent = self.agents[agent_name]
            if tool_name not in agent.tools:
                raise ValueError(f"Tool not found: {tool_name} on agent {agent_name}")
            
            tool = agent.tools[tool_name]
            if asyncio.iscoroutinefunction(tool.handler):
                result = await tool.handler(**arguments)
            else:
                result = tool.handler(**arguments)
            
            return {
                "result": {
                    "content": [{"text": json.dumps(result)}]
                }
            }
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return {
                "result": {
                    "content": [{"text": f"Error: {str(e)}"}],
                    "isError": True
                }
            }
    
    async def start_agents(self) -> None:
        """Start all required agents for workflow execution."""
        # Agents are initialized in initialize_agents, nothing special needed here
        logger.info(f"Started {len(self.agents)} agents")
    
    async def stop_all_agents(self) -> None:
        """Stop all running agents and cleanup resources."""
        await self.shutdown()
    
    async def execute_intelligent_workflow(self, user_request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an intelligent workflow based on user request."""
        try:
            await self.start_agents()
            
            # Plan the workflow
            workflow_steps = self.plan_workflow(user_request, context)
            if not workflow_steps:
                return {
                    "workflow": "intelligent_workflow",
                    "user_goal": user_request,
                    "steps_executed": 0,
                    "error": "Could not plan workflow for this request",
                    "summary": "Failed to plan workflow"
                }
            
            # Execute each step
            results = {}
            for i, step in enumerate(workflow_steps):
                resolved_args = self._resolve_arguments(step.arguments, results)
                
                step_result = await self.call_agent_tool(
                    step.agent_name, 
                    step.tool_name, 
                    resolved_args
                )
                
                results[f"step_{i}"] = step_result
                logger.info(f"Completed workflow step {i+1}/{len(workflow_steps)}")
            
            # Generate summary
            summary = self._generate_workflow_summary(workflow_steps, results)
            
            await self.stop_all_agents()
            
            return {
                "workflow": "intelligent_workflow",
                "user_goal": user_request,
                "steps_executed": len(workflow_steps),
                "summary": summary,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Intelligent workflow execution failed: {e}")
            await self.stop_all_agents()
            return {
                "workflow": "intelligent_workflow", 
                "user_goal": user_request,
                "steps_executed": 0,
                "error": str(e),
                "summary": "Workflow execution failed"
            }
    
    async def execute_adaptive_workflow(self, user_request: str, 
                                      available_agents: List[str],
                                      planning_method: Optional[str] = None) -> Dict[str, Any]:
        """Execute an adaptive workflow using the specified planning method."""
        try:
            from .planners import AdaptivePlanner
            
            # Initialize adaptive planner
            planner = AdaptivePlanner()
            
            # Create workflow using adaptive planning
            workflow_definition = await planner.create_workflow(
                user_request, 
                available_agents,
                planning_method=planning_method
            )
            
            # Execute the workflow
            workflow_result = await self.execute_workflow(
                workflow_definition.get("workflow_id", "adaptive_workflow"),
                workflow_definition
            )
            
            # Add planning information to result
            workflow_result.update({
                "planning_method": workflow_definition.get("planning_method", "unknown"),
                "planning_reason": workflow_definition.get("planning_reason", "No reason provided"),
                "user_request": user_request
            })
            
            return workflow_result
            
        except Exception as e:
            logger.error(f"Adaptive workflow execution failed: {e}")
            return {
                "workflow_id": "adaptive_workflow",
                "status": "failed",
                "error": str(e),
                "planning_method": planning_method or "unknown",
                "user_request": user_request
            }