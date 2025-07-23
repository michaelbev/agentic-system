#!/usr/bin/env python3
"""
Simplified test runner for the new Redaptive structure.
"""

import sys
import subprocess
import os
from pathlib import Path

def run_pytest(test_path: str, description: str) -> bool:
    """Run pytest on a specific path."""
    print(f"\n🧪 Running {description}")
    print("=" * 50)
    
    try:
        # Add src to path
        env = dict(os.environ)
        src_path = str(Path(__file__).parent.parent / "src")
        env['PYTHONPATH'] = src_path + ":" + env.get('PYTHONPATH', '')
        
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            test_path, 
            "-v", 
            "--tb=short",
            "--no-header"
        ], env=env, capture_output=False)
        
        success = result.returncode == 0
        print(f"✅ {description} PASSED" if success else f"❌ {description} FAILED")
        return success
        
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Run all test suites."""
    import os
    
    print("🤖 Redaptive Agentic Platform Test Suite")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    
    # Test suites to run
    test_suites = [
        ("tests/unit/test_config.py", "Configuration Tests"),
        ("tests/unit/test_agents.py", "Agent Tests"),
        ("tests/unit/test_orchestration.py", "Orchestration Tests"),
        ("tests/unit/test_tools.py", "Tools Tests"),
        ("tests/unit/test_streaming.py", "Streaming Tests"),
        ("tests/integration/test_platform.py", "Integration Tests"),
    ]
    
    results = []
    
    for test_path, description in test_suites:
        full_path = project_root / test_path
        if full_path.exists():
            success = run_pytest(str(full_path), description)
            results.append((description, success))
        else:
            print(f"⚠️  Test file not found: {test_path}")
            results.append((description, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description:30} : {status}")
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    exit(main())