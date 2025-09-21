#!/usr/bin/env python3
"""
Simple server startup script for the Docling backend.
This script helps resolve import issues on Windows.
"""

import sys
import os
import uvicorn

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if __name__ == "__main__":
    print("Starting Docling Backend Server...")
    print(f"Python path: {sys.path}")

    # Test docling import first
    try:
        import docling
        print(f"Docling found at: {docling.__file__}")
    except ImportError as e:
        print(f"Failed to import docling: {e}")
        sys.exit(1)

    # Import the app after setting up the path
    from app.main import app

    # Run the server
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,  # Disable reload to avoid multiprocessing issues
        log_level="info"
    )
