#!/usr/bin/env python3
"""
MCP Agents Test Script
Test all agents to ensure they work correctly with MCP protocol
"""

import asyncio
import json
import logging
import subprocess
import time
from typing import Dict, Any, List

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from redaptive.agents import AGENT_REGISTRY, list_agents

class MCPAgentTester:
    def __init__(self):
        self.processes = {}
        self.test_results = {}
        
    async def start_agent_process(self, agent_name: str) -> subprocess.Popen:
        """Start an agent as a subprocess"""
        print(f"🚀 Starting {agent_name} agent process...")
        
        # Start the agent process
        process = subprocess.Popen(
            [sys.executable, "start_agents.py", agent_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Wait a moment for the agent to start
        await asyncio.sleep(1)
        
        if process.poll() is None:
            print(f"✅ {agent_name} agent started successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start {agent_name} agent:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
    
    async def send_mcp_request(self, process: subprocess.Popen, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send an MCP request to an agent process"""
        try:
            # Send request
            request_json = json.dumps(request) + "\n"
            process.stdin.write(request_json)
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            if response_line:
                return json.loads(response_line.strip())
            else:
                return {"error": "No response received"}
        except Exception as e:
            return {"error": f"Communication error: {str(e)}"}
    
    async def test_agent_initialization(self, agent_name: str, process: subprocess.Popen) -> bool:
        """Test agent initialization"""
        print(f"🧪 Testing {agent_name} initialization...")
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = await self.send_mcp_request(process, init_request)
        
        if "result" in response and "serverInfo" in response["result"]:
            server_info = response["result"]["serverInfo"]
            print(f"✅ {agent_name} initialized: {server_info['name']} v{server_info['version']}")
            return True
        else:
            print(f"❌ {agent_name} initialization failed: {response}")
            return False
    
    async def test_agent_tools(self, agent_name: str, process: subprocess.Popen) -> bool:
        """Test agent tools listing"""
        print(f"🧪 Testing {agent_name} tools...")
        
        # Send tools/list request
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = await self.send_mcp_request(process, tools_request)
        
        if "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"✅ {agent_name} has {len(tools)} tools:")
            for tool in tools:
                print(f"  • {tool['name']}: {tool['description']}")
            return True
        else:
            print(f"❌ {agent_name} tools test failed: {response}")
            return False
    
    async def test_agent_tool_call(self, agent_name: str, process: subprocess.Popen, tool_name: str, arguments: Dict[str, Any]) -> bool:
        """Test calling a specific tool"""
        print(f"🧪 Testing {agent_name} tool call: {tool_name}")
        
        # Send tools/call request
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        response = await self.send_mcp_request(process, call_request)
        
        if "result" in response and "content" in response["result"]:
            content = response["result"]["content"]
            if content and "text" in content[0]:
                result = json.loads(content[0]["text"])
                if "error" not in result:
                    print(f"✅ {agent_name} {tool_name} call successful")
                    return True
                else:
                    print(f"⚠️ {agent_name} {tool_name} returned error: {result['error']}")
                    return False
            else:
                print(f"❌ {agent_name} {tool_name} call failed: {response}")
                return False
        else:
            print(f"❌ {agent_name} {tool_name} call failed: {response}")
            return False
    
    async def test_specific_agent_tools(self, agent_name: str, process: subprocess.Popen):
        """Test specific tools for each agent type"""
        if agent_name == "time":
            # Test time agent tools
            await self.test_agent_tool_call(agent_name, process, "get_current_time", {"timezone": "America/Denver"})
            await self.test_agent_tool_call(agent_name, process, "get_time_info", {"timezone": "Europe/London"})
            
        elif agent_name == "summarize":
            # Test summarize agent tools
            test_text = "This is a test text for summarization. It contains multiple sentences to test the summarization capabilities of the agent."
            await self.test_agent_tool_call(agent_name, process, "summarize_text", {"text": test_text, "max_length": 50})
            await self.test_agent_tool_call(agent_name, process, "analyze_sentiment", {"text": test_text, "detailed": False})
            
        elif agent_name == "db-admin":
            # Test database admin tools
            await self.test_agent_tool_call(agent_name, process, "list_tables", {})
            await self.test_agent_tool_call(agent_name, process, "get_database_stats", {})
            
        elif agent_name == "energy":
            # Test energy agent tools
            await self.test_agent_tool_call(agent_name, process, "analyze_consumption", {"building_id": 1})
            await self.test_agent_tool_call(agent_name, process, "get_usage_data", {"period": "2024-01"})
            
        elif agent_name == "textract":
            # Test textract agent tools (will fail without AWS credentials, but that's expected)
            await self.test_agent_tool_call(agent_name, process, "extract_text", {"file_path": "/nonexistent/file.pdf"})
    
    async def test_agent(self, agent_name: str) -> Dict[str, Any]:
        """Test a specific agent"""
        print(f"\n{'='*50}")
        print(f"🧪 Testing {agent_name} agent")
        print(f"{'='*50}")
        
        # Start agent process
        process = await self.start_agent_process(agent_name)
        if not process:
            return {"success": False, "error": "Failed to start agent process"}
        
        try:
            # Test initialization
            init_success = await self.test_agent_initialization(agent_name, process)
            if not init_success:
                return {"success": False, "error": "Initialization failed"}
            
            # Test tools listing
            tools_success = await self.test_agent_tools(agent_name, process)
            if not tools_success:
                return {"success": False, "error": "Tools listing failed"}
            
            # Test specific tools
            await self.test_specific_agent_tools(agent_name, process)
            
            return {"success": True, "message": f"{agent_name} agent tests completed"}
            
        finally:
            # Clean up process
            process.terminate()
            process.wait()
            print(f"👋 {agent_name} agent process terminated")
    
    async def test_all_agents(self):
        """Test all available agents"""
        print("🧪 Starting MCP Agents Test Suite")
        print("="*60)
        
        agents = list_agents()
        print(f"Found {len(agents)} agents: {', '.join(agents)}")
        
        for agent_name in agents:
            result = await self.test_agent(agent_name)
            self.test_results[agent_name] = result
            
            if result["success"]:
                print(f"✅ {agent_name}: PASSED")
            else:
                print(f"❌ {agent_name}: FAILED - {result.get('error', 'Unknown error')}")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for result in self.test_results.values() if result["success"])
        total = len(self.test_results)
        
        print(f"Total agents tested: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All agents passed! MCP implementation is working correctly.")
        else:
            print("\n⚠️ Some agents failed. Check the output above for details.")

async def main():
    """Main test function"""
    logging.basicConfig(level=logging.INFO)
    
    tester = MCPAgentTester()
    await tester.test_all_agents()

if __name__ == "__main__":
    import sys
    asyncio.run(main()) 