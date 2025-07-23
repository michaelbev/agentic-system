#!/usr/bin/env python3
"""
MCP Learning Setup Test
Verifies that all MCP learning components are working correctly
"""

import asyncio
import sys
import subprocess
import pytest
from pathlib import Path

def test_prerequisites():
    """Test if all prerequisites are installed"""
    print("🔍 Testing Prerequisites...")
    
    tests = [
        ("Python 3.11+", lambda: sys.version_info >= (3, 11)),
        ("uv", lambda: subprocess.run(["uv", "--version"], capture_output=True).returncode == 0),
        ("npx", lambda: subprocess.run(["npx", "--version"], capture_output=True).returncode == 0),
    ]
    
    all_passed = True
    for name, test_func in tests:
        try:
            if test_func():
                print(f"✅ {name}")
            else:
                print(f"❌ {name}")
                all_passed = False
        except Exception:
            print(f"❌ {name}")
            all_passed = False
    
    assert all_passed, "Not all prerequisites are available"

def test_files():
    """Test if all required files exist"""
    print("\n📁 Testing Files...")
    
    required_files = [
        "MCP_LEARNING_GUIDE.md",
        "working_mcp_client.py",
        "mcp_client_example.py",
        "orchestration/mcp_orchestrator.py",
        "requirements.txt",
        "mcp.json",
        ".env"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_exist = False
    
    assert all_exist, "Not all required files exist"

@pytest.mark.asyncio
async def test_mcp_time_server():
    """Test MCP time server connection"""
    print("\n🕐 Testing MCP Time Server...")
    
    try:
        # Test if uvx mcp-server-time is available
        result = subprocess.run(
            ["uvx", "mcp-server-time", "--help"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ MCP Time Server available")
        else:
            print("❌ MCP Time Server not available")
            assert False, "MCP Time Server not available"
            
    except subprocess.TimeoutExpired:
        print("❌ MCP Time Server test timed out")
        assert False, "MCP Time Server test timed out"
    except FileNotFoundError:
        print("❌ uvx not found")
        assert False, "uvx not found"
    except Exception as e:
        print(f"❌ Error testing MCP Time Server: {e}")
        assert False, f"Error testing MCP Time Server: {e}"

@pytest.mark.asyncio
async def test_working_client():
    """Test our working MCP client"""
    print("\n🔧 Testing Working MCP Client...")
    
    try:
        # Import the client
        sys.path.append(str(Path(__file__).parent.parent.parent / "scripts" / "mcp"))
        from working_mcp_client import WorkingMCPClient
        
        # Create client instance
        client = WorkingMCPClient(["uvx", "mcp-server-time", "--local-timezone=America/Denver"])
        
        # Test initialization
        if await client.start():
            print("✅ Working MCP Client initialized")
            
            # Test tool listing
            tools_response = await client.list_tools()
            if "result" in tools_response:
                tools = tools_response["result"]["tools"]
                print(f"✅ Found {len(tools)} tools")
                
                # Test tool calling
                if any(tool['name'] == 'get_current_time' for tool in tools):
                    time_response = await client.call_tool("get_current_time", {
                        "timezone": "America/Denver"
                    })
                    if "result" in time_response:
                        print("✅ Tool calling works")
                    else:
                        print("❌ Tool calling failed")
                else:
                    print("⚠️  get_current_time tool not found")
            
            await client.stop()
        else:
            print("❌ Working MCP Client failed to initialize")
            assert False, "Working MCP Client failed to initialize"
            
    except Exception as e:
        print(f"❌ Error testing Working MCP Client: {e}")
        assert False, f"Error testing Working MCP Client: {e}"

@pytest.mark.asyncio
async def test_mcp_orchestrator():
    """Test MCP orchestrator"""
    print("\n🚀 Testing MCP Orchestrator...")
    
    try:
        # Import orchestrator
        sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
        from redaptive.orchestration import OrchestrationEngine
        
        # Create orchestrator instance
        orchestrator = OrchestrationEngine()
        
        # Test agent configuration
        if "time" in orchestrator.agents:
            print("✅ Time agent configured")
        else:
            print("❌ Time agent not configured")
            return False
        
        # Test starting agents
        success = await orchestrator.start_agent("time")
        if success:
            print("✅ MCP Orchestrator can start agents")
            
            # Test tool discovery
            tools = await orchestrator.list_available_tools()
            if tools:
                print(f"✅ Found tools: {tools}")
            else:
                print("⚠️  No tools discovered")
            
            await orchestrator.stop_all_agents()
            return True
        else:
            print("❌ MCP Orchestrator failed to start agents")
            assert False, "MCP Orchestrator failed to start agents"
            
    except Exception as e:
        print(f"❌ Error testing MCP Orchestrator: {e}")
        assert False, f"Error testing MCP Orchestrator: {e}"

def test_mcp_inspector():
    """Test MCP Inspector availability"""
    print("\n🎯 Testing MCP Inspector...")
    
    try:
        # Check if MCP Inspector is available
        result = subprocess.run(
            ["npx", "@modelcontextprotocol/inspector", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ MCP Inspector available")
        else:
            print("❌ MCP Inspector not available")
            assert False, "MCP Inspector not available"
            
    except subprocess.TimeoutExpired:
        print("❌ MCP Inspector test timed out")
        assert False, "MCP Inspector test timed out"
    except FileNotFoundError:
        print("❌ npx not found")
        assert False, "npx not found"
    except Exception as e:
        print(f"❌ Error testing MCP Inspector: {e}")
        assert False, f"Error testing MCP Inspector: {e}"

async def main():
    """Run all tests"""
    print("🎓 MCP Learning Setup Test")
    print("=" * 40)
    
    # Test prerequisites
    prereq_ok = test_prerequisites()
    
    # Test files
    files_ok = test_files()
    
    # Test MCP components
    time_server_ok = await test_mcp_time_server()
    working_client_ok = await test_working_client()
    orchestrator_ok = await test_mcp_orchestrator()
    inspector_ok = test_mcp_inspector()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"Prerequisites: {'✅' if prereq_ok else '❌'}")
    print(f"Files: {'✅' if files_ok else '❌'}")
    print(f"MCP Time Server: {'✅' if time_server_ok else '❌'}")
    print(f"Working Client: {'✅' if working_client_ok else '❌'}")
    print(f"MCP Orchestrator: {'✅' if orchestrator_ok else '❌'}")
    print(f"MCP Inspector: {'✅' if inspector_ok else '❌'}")
    
    all_tests_passed = all([
        prereq_ok, files_ok, time_server_ok, 
        working_client_ok, orchestrator_ok, inspector_ok
    ])
    
    if all_tests_passed:
        print("\n🎉 All tests passed! Your MCP learning environment is ready.")
        print("\n🚀 Next steps:")
        print("1. Run: python start_orchestration.py")
        print("2. Choose option 1 to test the time server")
        print("3. Choose option 3 to use MCP Inspector")
        print("4. Read MCP_LEARNING_GUIDE.md for detailed learning path")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\n🔧 Common fixes:")
        print("1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("2. Install Node.js for MCP Inspector")
        print("3. Check that all files exist in the project directory")

if __name__ == "__main__":
    asyncio.run(main()) 