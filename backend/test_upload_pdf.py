#!/usr/bin/env python3
"""
Test script to upload a PDF document to the Docling backend.
"""

import requests
import os
import sys
from pathlib import Path

def test_upload():
    """Test uploading a PDF document."""
    
    # Check if we have a PDF file to test with
    test_files = [
        "test_document.pdf",
        "REFACTOR_PLAN.pdf", 
        "Invoice 113675190.pdf"
    ]
    
    test_file = None
    for filename in test_files:
        if os.path.exists(filename):
            test_file = filename
            break
    
    if not test_file:
        print("❌ No test PDF file found. Please provide a PDF file to test with.")
        print(f"Looking for: {test_files}")
        return False
    
    print(f"📄 Using test file: {test_file}")
    
    # Upload the document
    url = "http://127.0.0.1:8000/api/upload"
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': (test_file, f, 'application/pdf')}
            print(f"🚀 Uploading {test_file}...")
            
            response = requests.post(url, files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                job_id = result.get('job_id')
                print(f"✅ Upload successful!")
                print(f"📋 Job ID: {job_id}")
                print(f"📊 Response: {result}")
                
                # Test status endpoint
                status_url = f"http://127.0.0.1:8000/api/status/{job_id}"
                print(f"\n🔍 Checking status...")
                
                status_response = requests.get(status_url, timeout=10)
                if status_response.status_code == 200:
                    status_result = status_response.json()
                    print(f"✅ Status check successful!")
                    print(f"📊 Status: {status_result}")
                else:
                    print(f"❌ Status check failed: {status_response.status_code}")
                    print(f"📄 Response: {status_response.text}")
                
                return True
                
            else:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"📄 Response: {response.text}")
                return False
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {test_file}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Docling PDF Upload...")
    success = test_upload()
    sys.exit(0 if success else 1)
