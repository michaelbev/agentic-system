# MCP (Model Context Protocol) Learning Guide

## What is MCP?

The **Model Context Protocol (MCP)** is a standardized protocol that enables AI assistants to securely access external tools and data sources. It's designed specifically for AI agents and provides a structured way for LLMs to interact with external systems.

## Key MCP Concepts

### 1. **Protocol Structure**
MCP uses **JSON-RPC 2.0** as its base protocol with specific message formats:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {...},
    "clientInfo": {...}
  }
}
```

### 2. **Core Components**

#### **Servers**
- Provide tools, resources, and prompts
- Run as separate processes
- Communicate via stdin/stdout
- Examples: Time server, Filesystem server, Git server

#### **Clients**
- Consume tools and resources
- Examples: Claude, VS Code, custom applications

#### **Tools**
- Functions that can be called by clients
- Have defined parameters and return values
- Examples: `get_current_time`, `convert_time`

### 3. **MCP Protocol Flow**

```
1. Client starts server process
2. Client sends "initialize" request
3. Server responds with capabilities
4. Client sends "notifications/initialized"
5. Client can now call tools
```

## Learning MCP Step by Step

### Step 1: Use the MCP Inspector

The MCP Inspector is the best tool for learning MCP:

```bash
# Install and run the inspector
npx @modelcontextprotocol/inspector uvx mcp-server-time

# This will:
# - Start a proxy server
# - Open a web interface
# - Show you the exact protocol messages
# - Let you test tools interactively
```

### Step 2: Understand the Protocol Messages

#### **Initialize Request**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {},
      "resources": {},
      "prompts": {}
    },
    "clientInfo": {
      "name": "my-client",
      "version": "1.0.0"
    }
  }
}
```

#### **Initialize Response**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {
        "listChanged": false
      }
    },
    "serverInfo": {
      "name": "mcp-time",
      "version": "1.10.1"
    }
  }
}
```

#### **List Tools Request**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

#### **Call Tool Request**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_current_time",
    "arguments": {
      "timezone": "America/Denver"
    }
  }
}
```

### Step 3: Build Your Own MCP Client

Here's a minimal working MCP client:

```python
import asyncio
import json
import subprocess

class SimpleMCPClient:
    def __init__(self, server_command):
        self.server_command = server_command
        self.process = None
        
    async def start(self):
        # Start server process
        self.process = await asyncio.create_subprocess_exec(
            *self.server_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )
        
        # Initialize
        await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
            "clientInfo": {"name": "simple-client", "version": "1.0.0"}
        })
        
        # Send initialized notification
        await self._send_request("notifications/initialized", {})
        
    async def _send_request(self, method, params):
        request = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        self.process.stdin.write((json.dumps(request) + "\n").encode())
        await self.process.stdin.drain()
        
        response = await self.process.stdout.readline()
        return json.loads(response.decode())
        
    async def call_tool(self, name, arguments):
        return await self._send_request("tools/call", {"name": name, "arguments": arguments})
```

### Step 4: Build Your Own MCP Server

Create a simple MCP server:

```python
import asyncio
import json
import sys
from datetime import datetime

class SimpleMCPServer:
    def __init__(self):
        self.initialized = False
        
    async def handle_request(self, request):
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            return self._handle_initialize(params)
        elif method == "tools/list":
            return self._handle_tools_list()
        elif method == "tools/call":
            return await self._handle_tool_call(params)
        else:
            return {"error": {"code": -32601, "message": "Method not found"}}
    
    def _handle_initialize(self, params):
        self.initialized = True
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "simple-server", "version": "1.0.0"}
            }
        }
    
    def _handle_tools_list(self):
        return {
            "jsonrpc": "2.0",
            "id": 2,
            "result": {
                "tools": [
                    {
                        "name": "get_time",
                        "description": "Get current time",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "timezone": {"type": "string"}
                            }
                        }
                    }
                ]
            }
        }
    
    async def _handle_tool_call(self, params):
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "get_time":
            timezone = arguments.get("timezone", "UTC")
            current_time = datetime.now().isoformat()
            return {
                "jsonrpc": "2.0",
                "id": 3,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Current time in {timezone}: {current_time}"
                        }
                    ]
                }
            }
        else:
            return {"error": {"code": -32601, "message": "Tool not found"}}

async def main():
    server = SimpleMCPServer()
    
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
            
        request = json.loads(line)
        response = await server.handle_request(request)
        
        print(json.dumps(response))
        sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())
```

## MCP vs HTTP: When to Use Each

### **Use MCP When:**
- Building tools for **AI assistants** (Claude, ChatGPT)
- Need **structured, AI-optimized** responses
- Want **standard MCP client** compatibility
- Building **standalone tools** for LLMs

### **Use HTTP When:**
- Building **web applications**
- Need **standard REST APIs**
- Want **easy monitoring** and debugging
- Building **microservices** for web clients

## Next Steps for Learning

1. **Use the MCP Inspector** to explore existing servers
2. **Build a simple MCP client** to understand the protocol
3. **Create your own MCP server** for a specific domain
4. **Build MCP orchestration** - Create systems that coordinate multiple MCP servers
5. **Integrate with AI** - Connect your MCP servers to AI assistants

## Resources

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## Your Learning Path

Since you want to learn MCP:

1. **Start with the Inspector** - Use it to understand how MCP works
2. **Build simple clients** - Create basic MCP clients
3. **Create custom servers** - Build MCP servers for your domains
4. **Build MCP orchestration** - Create systems that coordinate multiple MCP servers
5. **Integrate with AI** - Connect your MCP servers to AI assistants

This approach will give you deep understanding of the MCP protocol and how to build AI-native tools! 🚀 