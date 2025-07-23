#!/usr/bin/env python3
"""
Base MCP Server Template
Provides common functionality for all MCP agents following the official MCP protocol
"""

import asyncio
import json
import sys
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MCPTool:
    name: str
    description: str
    handler: Callable
    input_schema: Dict[str, Any]

class BaseMCPServer:
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, MCPTool] = {}
        self.initialized = False
        self.logger = logging.getLogger(name)
        
    def register_tool(self, name: str, description: str, handler: Callable, input_schema: Dict[str, Any]):
        """Register a tool with the MCP server"""
        self.tools[name] = MCPTool(
            name=name,
            description=description,
            handler=handler,
            input_schema=input_schema
        )
        self.logger.info(f"Registered tool: {name}")
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP protocol requests"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return await self._handle_initialize(params, request_id)
            elif method == "tools/list":
                return await self._handle_tools_list(request_id)
            elif method == "tools/call":
                return await self._handle_tool_call(params, request_id)
            elif method == "notifications/initialized":
                # No response needed for notifications
                return None
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            self.logger.error(f"Error handling request: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def _handle_initialize(self, params: Dict[str, Any], request_id: int) -> Dict[str, Any]:
        """Handle initialize request"""
        self.initialized = True
        self.logger.info(f"Initialized {self.name} server")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    }
                },
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }
        }
    
    async def _handle_tools_list(self, request_id: int) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools_list = []
        for tool in self.tools.values():
            tools_list.append({
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            })
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools_list
            }
        }
    
    async def _handle_tool_call(self, params: Dict[str, Any], request_id: int) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}"
                }
            }
        
        try:
            tool = self.tools[tool_name]
            
            # Call the tool handler
            if asyncio.iscoroutinefunction(tool.handler):
                result = await tool.handler(**arguments)
            else:
                result = tool.handler(**arguments)
            
            # Format the response according to MCP protocol
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ],
                    "isError": False
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error executing tool {tool_name}: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({"error": str(e)}, indent=2)
                        }
                    ],
                    "isError": True
                }
            }
    
    async def run(self):
        """Run the MCP server"""
        self.logger.info(f"Starting {self.name} MCP server...")
        
        while True:
            try:
                # Read request from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                # Parse request
                request = json.loads(line.strip())
                
                # Handle request
                response = await self.handle_request(request)
                
                # Send response if not a notification
                if response:
                    print(json.dumps(response))
                    sys.stdout.flush()
                    
            except json.JSONDecodeError as e:
                self.logger.error(f"Invalid JSON: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                break
        
        self.logger.info(f"{self.name} MCP server stopped")

# Example usage:
"""
class TimeServer(BaseMCPServer):
    def __init__(self):
        super().__init__("time-server", "1.0.0")
        self.setup_tools()
        
    def setup_tools(self):
        self.register_tool(
            "get_current_time",
            "Get current time in specified timezone",
            self.get_current_time,
            {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA timezone name"
                    }
                },
                "required": ["timezone"]
            }
        )
        
    async def get_current_time(self, timezone: str):
        from datetime import datetime
        import pytz
        
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return {
            "timezone": timezone,
            "datetime": now.isoformat(),
            "is_dst": now.dst() is not None and now.dst().total_seconds() > 0
        }

if __name__ == "__main__":
    server = TimeServer()
    asyncio.run(server.run())
""" 