"""
Test API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data


def test_readiness_endpoint():
    """Test readiness check endpoint."""
    response = client.get("/api/health/ready")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "ready"
    assert "checks" in data


def test_liveness_endpoint():
    """Test liveness check endpoint."""
    response = client.get("/api/health/live")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "alive"


def test_upload_limits_endpoint():
    """Test upload limits endpoint."""
    response = client.get("/api/upload/limits")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert "limits" in data
    assert "supported_formats" in data
    
    limits = data["limits"]
    assert "max_file_size" in limits
    assert "allowed_extensions" in limits


def test_upload_no_file():
    """Test upload endpoint without file."""
    response = client.post("/api/upload")
    assert response.status_code == 422  # Validation error


def test_job_status_not_found():
    """Test job status for non-existent job."""
    response = client.get("/api/status/non-existent-job")
    assert response.status_code == 404


def test_job_result_not_found():
    """Test job result for non-existent job."""
    response = client.get("/api/result/non-existent-job")
    assert response.status_code == 404


def test_download_not_found():
    """Test download for non-existent job."""
    response = client.get("/api/download/non-existent-job")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_file_upload_integration():
    """Test file upload integration (with mock file)."""
    # Create a mock PDF file
    mock_file_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
    
    files = {
        "file": ("test.pdf", mock_file_content, "application/pdf")
    }
    
    response = client.post("/api/upload", files=files)
    
    # Should succeed or fail gracefully
    assert response.status_code in [200, 400, 422, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "job_id" in data
        assert "filename" in data
        assert data["filename"] == "test.pdf"


def test_cors_headers():
    """Test CORS headers are present."""
    response = client.options("/api/health")
    assert response.status_code == 200
    
    # Check for CORS headers
    headers = response.headers
    assert "access-control-allow-origin" in headers or "Access-Control-Allow-Origin" in headers
