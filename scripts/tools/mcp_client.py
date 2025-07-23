#!/usr/bin/env python3
"""
Production MCP Client

A robust, production-ready MCP client for testing and interacting with MCP servers.
Supports all MCP protocol features with comprehensive error handling.
"""

import asyncio
import json
import subprocess
import sys
import time
from typing import Dict, Any, Optional, List
import argparse

class ProductionMCPClient:
    """Production-ready MCP client with comprehensive error handling"""
    
    def __init__(self, server_command: List[str], debug: bool = False):
        self.server_command = server_command
        self.process = None
        self.request_id = 1
        self.debug = debug
        self.tools = {}
        
    async def start(self):
        """Start the MCP server and initialize connection"""
        print(f"🚀 Starting MCP server: {' '.join(self.server_command)}")
        
        try:
            # Start server process
            self.process = await asyncio.create_subprocess_exec(
                *self.server_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Initialize connection
            await self._initialize_connection()
            
            # Discover available tools
            await self._discover_tools()
            
            print("✅ MCP client ready")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start MCP server: {e}")
            return False
    
    async def stop(self):
        """Stop the MCP server and cleanup"""
        if self.process:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()
            print("👋 MCP server stopped")
    
    async def _initialize_connection(self):
        """Initialize the MCP connection"""
        init_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {}
                },
                "clientInfo": {
                    "name": "production-mcp-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = await self._send_request(init_request)
        if self.debug:
            print(f"🔍 Initialize response: {response}")
        
        if "error" in response:
            raise Exception(f"Initialization failed: {response['error']}")
        
        self.request_id += 1
    
    async def _discover_tools(self):
        """Discover available tools from the server"""
        tools_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list",
            "params": {}
        }
        
        response = await self._send_request(tools_request)
        if self.debug:
            print(f"🔍 Tools list response: {response}")
        
        if "error" in response:
            print(f"⚠️ Could not discover tools: {response['error']}")
            return
        
        if "result" in response and "tools" in response["result"]:
            for tool in response["result"]["tools"]:
                self.tools[tool["name"]] = tool
        
        self.request_id += 1
    
    async def _send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to the MCP server and get response"""
        if not self.process or not self.process.stdin:
            raise Exception("MCP server not running")
        
        # Send request
        request_line = json.dumps(request) + '\n'
        if self.debug:
            print(f"📤 Sending: {request_line.strip()}")
        
        self.process.stdin.write(request_line.encode())
        await self.process.stdin.drain()
        
        # Read response
        try:
            response_line = await asyncio.wait_for(
                self.process.stdout.readline(), 
                timeout=30.0
            )
            
            if not response_line:
                raise Exception("No response from server")
            
            response_text = response_line.decode().strip()
            if self.debug:
                print(f"📥 Received: {response_text}")
            
            return json.loads(response_text)
            
        except asyncio.TimeoutError:
            raise Exception("Request timeout")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {e}")
    
    async def list_tools(self) -> Dict[str, Any]:
        """List all available tools"""
        return self.tools
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a specific tool with arguments"""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}
        
        if arguments is None:
            arguments = {}
        
        call_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        response = await self._send_request(call_request)
        self.request_id += 1
        
        return response
    
    async def interactive_mode(self):
        """Run in interactive mode for testing"""
        print("\n🎮 Interactive MCP Client Mode")
        print("Commands:")
        print("  list - List available tools")
        print("  call <tool_name> [args] - Call a tool")
        print("  debug - Toggle debug mode")
        print("  quit - Exit")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if command == "quit":
                    break
                elif command == "list":
                    await self._interactive_list_tools()
                elif command == "debug":
                    self.debug = not self.debug
                    print(f"🔧 Debug mode: {'ON' if self.debug else 'OFF'}")
                elif command.startswith("call "):
                    await self._interactive_call_tool(command[5:])
                elif command == "help":
                    print("Available commands: list, call <tool> [args], debug, quit")
                elif command:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def _interactive_list_tools(self):
        """Interactive tool listing"""
        if not self.tools:
            print("No tools available")
            return
        
        print(f"\n📋 Available tools ({len(self.tools)}):")
        for name, tool in self.tools.items():
            desc = tool.get("description", "No description")
            print(f"  • {name}: {desc}")
    
    async def _interactive_call_tool(self, command: str):
        """Interactive tool calling"""
        parts = command.split(maxsplit=1)
        tool_name = parts[0]
        
        if tool_name not in self.tools:
            print(f"❌ Tool '{tool_name}' not found")
            return
        
        # Parse arguments if provided
        arguments = {}
        if len(parts) > 1:
            try:
                arguments = json.loads(parts[1])
            except json.JSONDecodeError:
                print("❌ Arguments must be valid JSON")
                return
        
        print(f"🔄 Calling {tool_name}...")
        result = await self.call_tool(tool_name, arguments)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        elif "result" in result:
            print(f"✅ Result: {json.dumps(result['result'], indent=2)}")
        else:
            print(f"📋 Response: {json.dumps(result, indent=2)}")

async def test_time_server():
    """Test the official MCP time server"""
    print("🕐 Testing official MCP time server...")
    
    client = ProductionMCPClient(["uvx", "mcp-server-time"])
    
    try:
        if not await client.start():
            return False
        
        # List tools
        tools = await client.list_tools()
        print(f"📋 Available tools: {', '.join(tools.keys())}")
        
        # Test get_current_time
        if "get_current_time" in tools:
            result = await client.call_tool("get_current_time", {"timezone": "America/Denver"})
            if "result" in result:
                print(f"✅ Current time: {result['result']}")
            else:
                print(f"❌ Time call failed: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        await client.stop()

async def test_energy_agent():
    """Test the energy agent"""
    print("🔋 Testing energy agent...")
    
    client = ProductionMCPClient(["python", "start_agents.py", "energy"])
    
    try:
        if not await client.start():
            return False
        
        # List tools
        tools = await client.list_tools()
        print(f"📋 Available tools: {', '.join(tools.keys())}")
        
        # Test search_facilities
        if "search_facilities" in tools:
            result = await client.call_tool("search_facilities", {"location": "Dallas"})
            if "result" in result:
                print(f"✅ Facility search: {result['result']}")
            else:
                print(f"❌ Facility search failed: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        await client.stop()

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Production MCP Client")
    parser.add_argument("--server", nargs="+", help="MCP server command", 
                       default=["uvx", "mcp-server-time"])
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--debug", action="store_true", 
                       help="Enable debug output")
    parser.add_argument("--test", choices=["time", "energy", "all"], 
                       help="Run specific tests")
    
    args = parser.parse_args()
    
    async def run():
        if args.test:
            if args.test == "time" or args.test == "all":
                success = await test_time_server()
                if not success:
                    return 1
            
            if args.test == "energy" or args.test == "all":
                success = await test_energy_agent()
                if not success:
                    return 1
            
            print("✅ All tests completed successfully")
            return 0
        
        # Regular client mode
        client = ProductionMCPClient(args.server, debug=args.debug)
        
        try:
            if not await client.start():
                return 1
            
            if args.interactive:
                await client.interactive_mode()
            else:
                # Quick demo
                tools = await client.list_tools()
                print(f"📋 Available tools: {', '.join(tools.keys())}")
                
                # Call first tool if available
                if tools:
                    first_tool = next(iter(tools))
                    print(f"🔄 Testing {first_tool}...")
                    result = await client.call_tool(first_tool)
                    print(f"📋 Result: {json.dumps(result, indent=2)}")
            
            return 0
            
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user")
            return 0
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
        finally:
            await client.stop()
    
    return asyncio.run(run())

if __name__ == "__main__":
    exit(main())