#!/usr/bin/env python3
"""
Test script to upload a document and check job status.
"""
import requests
import time
import json

def test_upload_and_status():
    """Test document upload and status checking."""
    
    # Test file content
    test_content = """
    This is a test document for the Docling document processing application.
    
    It contains some sample text to test the document processing functionality.
    
    The document should be processed successfully with the updated transformers library.
    """
    
    # Create a test file
    with open("test_doc.txt", "w") as f:
        f.write(test_content)
    
    try:
        # Upload the document
        print("Uploading document...")
        with open("test_doc.txt", "rb") as f:
            files = {"file": ("test_doc.txt", f, "text/plain")}
            response = requests.post("http://127.0.0.1:8000/api/upload", files=files)
        
        if response.status_code == 200:
            upload_result = response.json()
            job_id = upload_result["job_id"]
            print(f"✅ Upload successful! Job ID: {job_id}")
            
            # Check job status
            print("Checking job status...")
            for i in range(10):  # Check for up to 10 times
                status_response = requests.get(f"http://127.0.0.1:8000/api/status/{job_id}")
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"✅ Status check {i+1}: {status_data['status']} - Progress: {status_data['progress']}%")
                    
                    if status_data["status"] in ["completed", "failed"]:
                        if status_data["status"] == "completed":
                            print("🎉 Document processing completed successfully!")
                        else:
                            print(f"❌ Document processing failed: {status_data.get('error', 'Unknown error')}")
                        break
                else:
                    print(f"❌ Status check {i+1} failed: {status_response.status_code} - {status_response.text}")
                
                time.sleep(2)  # Wait 2 seconds before next check
            else:
                print("⏰ Status checking timed out")
                
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
    
    finally:
        # Clean up test file
        import os
        if os.path.exists("test_doc.txt"):
            os.remove("test_doc.txt")

if __name__ == "__main__":
    test_upload_and_status()
