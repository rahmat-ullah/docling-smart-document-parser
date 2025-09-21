#!/usr/bin/env python3
"""
Check the status of a document processing job.
"""

import requests
import time
import sys

def check_status(job_id, max_checks=10):
    """Check job status periodically."""
    
    for i in range(max_checks):
        try:
            response = requests.get(f"http://127.0.0.1:8000/api/status/{job_id}", timeout=10)
            if response.status_code == 200:
                status = response.json()
                print(f"Check {i+1}: {status}")
                
                if status.get('status') == 'completed':
                    print("✅ Job completed successfully!")
                    
                    # Try to get results
                    results_response = requests.get(f"http://127.0.0.1:8000/api/result/{job_id}", timeout=10)
                    if results_response.status_code == 200:
                        results = results_response.json()
                        print(f"📊 Results: {results}")
                    else:
                        print(f"❌ Failed to get results: {results_response.status_code}")
                    
                    return True
                    
                elif status.get('status') == 'failed':
                    print("❌ Job failed!")
                    return False
                    
            else:
                print(f"❌ Status check failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking status: {e}")
            
        if i < max_checks - 1:
            time.sleep(5)
    
    print("⏰ Timeout waiting for job completion")
    return False

if __name__ == "__main__":
    job_id = "8868b02f-6e6d-4ee7-9ce6-c59ec683dbae"
    if len(sys.argv) > 1:
        job_id = sys.argv[1]
    
    print(f"🔍 Checking status for job: {job_id}")
    check_status(job_id)
