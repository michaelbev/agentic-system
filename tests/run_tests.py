#!/usr/bin/env python3
"""
Test runner for the Intelligent Orchestrator
Runs all tests and provides a summary
"""

import asyncio
import sys
import subprocess
from pathlib import Path

def run_pytest_tests():
    """Run the pytest test suite"""
    print("🧪 Running Intelligent Orchestrator Tests")
    print("=" * 50)
    
    # Run pytest with verbose output
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/unit/test_intelligent_orchestrator.py", 
        "-v", 
        "--tb=short"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

def run_unit_tests():
    """Run the unit tests"""
    print("\n🧪 Running Unit Tests")
    print("=" * 25)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/unit/", "-v"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Unit tests failed: {e}")
        return False

def run_integration_tests():
    """Run the integration tests"""
    print("\n🔗 Running Integration Tests")
    print("=" * 30)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/integration/", "-v"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Integration tests failed: {e}")
        return False

def run_setup_tests():
    """Run the setup validation tests"""
    print("\n⚙️  Running Setup Tests")
    print("=" * 25)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/setup/", "-v"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Setup tests failed: {e}")
        return False

def main():
    """Run all tests and provide summary"""
    print("🤖 Intelligent Orchestrator Test Suite")
    print("=" * 50)
    
    results = {}
    
    # Run pytest tests
    results["pytest"] = run_pytest_tests()
    
    # Run unit tests
    results["unit"] = run_unit_tests()
    
    # Run integration tests
    results["integration"] = run_integration_tests()
    
    # Run setup tests
    results["setup"] = run_setup_tests()
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:12} : {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\nOverall: {total_passed}/{total_tests} test suites passed")
    
    if total_passed == total_tests:
        print("🎉 All tests passed! The intelligent orchestrator is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    exit(main()) 