#!/usr/bin/env python3
"""
Test script to verify that all dependencies are correctly installed.
Run this script after installing requirements.txt to ensure everything works.
"""

import sys
import importlib
import traceback
from pathlib import Path

def test_import(module_name, description=""):
    """Test if a module can be imported."""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} - {description}")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - {description}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name} - {description}: Unexpected error: {e}")
        return False

def test_docling():
    """Test Docling specifically."""
    try:
        from docling.document_converter import DocumentConverter
        converter = DocumentConverter()
        print("✅ Docling DocumentConverter initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Docling initialization failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all dependency tests."""
    print("🔍 Testing Python Dependencies for Docling Application")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 9):
        print("❌ Python 3.9+ is required")
        return False
    elif python_version >= (3, 11):
        print("✅ Python version is optimal for Docling")
    else:
        print("⚠️  Python 3.11+ is recommended for optimal performance")
    
    print("\n📦 Testing Core Dependencies:")
    print("-" * 40)
    
    # Core dependencies
    dependencies = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("pydantic", "Data validation"),
        ("pydantic_settings", "Settings management"),
        ("multipart", "File upload support"),
        ("aiofiles", "Async file operations"),
        ("httpx", "HTTP client"),
        ("structlog", "Structured logging"),
        ("pytest", "Testing framework"),
    ]
    
    success_count = 0
    for module, desc in dependencies:
        if test_import(module, desc):
            success_count += 1
    
    print(f"\nCore dependencies: {success_count}/{len(dependencies)} successful")
    
    print("\n🤖 Testing ML Dependencies:")
    print("-" * 40)
    
    # ML dependencies
    ml_dependencies = [
        ("torch", "PyTorch deep learning framework"),
        ("torchvision", "Computer vision for PyTorch"),
        ("transformers", "Hugging Face Transformers"),
        ("accelerate", "Hugging Face Accelerate"),
        ("sentencepiece", "Text tokenization"),
        ("PIL", "Python Imaging Library (Pillow)"),
    ]
    
    ml_success_count = 0
    for module, desc in ml_dependencies:
        if test_import(module, desc):
            ml_success_count += 1
    
    print(f"\nML dependencies: {ml_success_count}/{len(ml_dependencies)} successful")
    
    print("\n📄 Testing Docling:")
    print("-" * 40)
    
    docling_success = test_docling()
    
    print("\n📊 Summary:")
    print("=" * 60)
    
    total_deps = len(dependencies) + len(ml_dependencies)
    total_success = success_count + ml_success_count
    
    print(f"Dependencies: {total_success}/{total_deps} successful")
    print(f"Docling: {'✅ Working' if docling_success else '❌ Failed'}")
    
    if total_success == total_deps and docling_success:
        print("\n🎉 All dependencies are working correctly!")
        print("You can now run the application with:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        return True
    else:
        print("\n⚠️  Some dependencies failed. Please check the errors above.")
        print("Try running: pip install -r requirements.txt --upgrade")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
