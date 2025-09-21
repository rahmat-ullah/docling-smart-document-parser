#!/usr/bin/env python3
"""
Integration test script to verify the complete application setup.
"""
import os
import sys
import subprocess
import time
import requests
import json
from pathlib import Path


def run_command(command, cwd=None, timeout=30):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"


def test_backend_setup():
    """Test backend setup and dependencies."""
    print("Testing backend setup...")
    
    # Check if backend directory exists
    if not Path("backend").exists():
        print("❌ Backend directory not found")
        return False
    
    # Test Python imports
    success, stdout, stderr = run_command(
        "python test_setup.py",
        cwd="backend"
    )
    
    if success:
        print("✅ Backend setup test passed")
        return True
    else:
        print(f"❌ Backend setup test failed: {stderr}")
        return False


def test_frontend_setup():
    """Test frontend setup and dependencies."""
    print("Testing frontend setup...")
    
    # Check if frontend directory exists
    if not Path("frontend").exists():
        print("❌ Frontend directory not found")
        return False
    
    # Check if node_modules exists or can install
    if not Path("frontend/node_modules").exists():
        print("Installing frontend dependencies...")
        success, stdout, stderr = run_command(
            "npm install",
            cwd="frontend",
            timeout=120
        )
        
        if not success:
            print(f"❌ Failed to install frontend dependencies: {stderr}")
            return False
    
    # Test TypeScript compilation
    success, stdout, stderr = run_command(
        "npm run type-check",
        cwd="frontend"
    )
    
    if success:
        print("✅ Frontend TypeScript compilation passed")
        return True
    else:
        print(f"❌ Frontend TypeScript compilation failed: {stderr}")
        return False


def test_docker_setup():
    """Test Docker setup."""
    print("Testing Docker setup...")
    
    # Check if docker-compose.yml exists
    if not Path("docker-compose.yml").exists():
        print("❌ docker-compose.yml not found")
        return False
    
    # Test docker-compose config
    success, stdout, stderr = run_command("docker-compose config")
    
    if success:
        print("✅ Docker Compose configuration is valid")
        return True
    else:
        print(f"❌ Docker Compose configuration failed: {stderr}")
        return False


def test_api_endpoints():
    """Test API endpoints (if backend is running)."""
    print("Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint is working")
            
            # Test upload limits endpoint
            response = requests.get(f"{base_url}/api/upload/limits", timeout=5)
            if response.status_code == 200:
                print("✅ Upload limits endpoint is working")
                return True
            else:
                print(f"❌ Upload limits endpoint failed: {response.status_code}")
                return False
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  API endpoints not accessible (backend may not be running): {e}")
        return None  # Not a failure, just not running


def main():
    """Run all tests."""
    print("=" * 60)
    print("Docling Document Processing Application - Integration Test")
    print("=" * 60)
    
    tests = [
        ("Backend Setup", test_backend_setup),
        ("Frontend Setup", test_frontend_setup),
        ("Docker Setup", test_docker_setup),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, result in results:
        if result is True:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        elif result is False:
            print(f"❌ {test_name}: FAILED")
            failed += 1
        else:
            print(f"⚠️  {test_name}: SKIPPED")
            skipped += 1
    
    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n🎉 All critical tests passed! The application setup is ready.")
        print("\nNext steps:")
        print("1. Start the backend: cd backend && python -m uvicorn app.main:app --reload")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Open http://localhost:3000 in your browser")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
