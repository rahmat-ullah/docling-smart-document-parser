#!/usr/bin/env python3
"""
Test script to verify backend setup and dependencies.
"""
import sys
import importlib
import traceback


def test_imports():
    """Test if all required packages can be imported."""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'pydantic_settings',
        'aiofiles',
        'python_multipart',
        'docling',
        'transformers',
        'torch',
        'PIL',
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✓ {package}")
        except ImportError as e:
            print(f"✗ {package}: {str(e)}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    else:
        print("\nAll packages imported successfully!")
        return True


def test_app_import():
    """Test if the FastAPI app can be imported."""
    print("\nTesting FastAPI app import...")
    try:
        from app.main import app
        print("✓ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import FastAPI app: {str(e)}")
        traceback.print_exc()
        return False


def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from app.core.config import settings
        print(f"✓ Configuration loaded")
        print(f"  - App name: {settings.app_name}")
        print(f"  - Environment: {settings.environment}")
        print(f"  - Debug: {settings.debug}")
        print(f"  - Docling model: {settings.docling_model}")
        return True
    except Exception as e:
        print(f"✗ Failed to load configuration: {str(e)}")
        traceback.print_exc()
        return False


def test_docling_basic():
    """Test basic Docling functionality."""
    print("\nTesting Docling basic functionality...")
    try:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        print("✓ Docling DocumentConverter created successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to create Docling converter: {str(e)}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Backend Setup Verification")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_app_import,
        test_docling_basic,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {str(e)}")
            results.append(False)
        print()
    
    # Summary
    print("=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Backend setup is ready.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
