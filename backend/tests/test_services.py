"""
Test service layer components.
"""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch
from fastapi import UploadFile
from io import BytesIO

from app.services.file_handler import FileHandler
from app.services.job_manager import JobManager
from app.core.exceptions import ValidationError, FileError


class TestFileHandler:
    """Test FileHandler service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.file_handler = FileHandler()
    
    @pytest.mark.asyncio
    async def test_validate_file_size_too_large(self):
        """Test file size validation."""
        # Create mock file that's too large
        mock_file = Mock(spec=UploadFile)
        mock_file.size = 100 * 1024 * 1024  # 100MB
        mock_file.filename = "test.pdf"
        
        with pytest.raises(ValidationError) as exc_info:
            await self.file_handler.validate_file(mock_file)
        
        assert "exceeds maximum allowed size" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_validate_file_no_filename(self):
        """Test validation with no filename."""
        mock_file = Mock(spec=UploadFile)
        mock_file.size = 1024
        mock_file.filename = None
        
        with pytest.raises(ValidationError) as exc_info:
            await self.file_handler.validate_file(mock_file)
        
        assert "Filename is required" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_validate_file_invalid_extension(self):
        """Test validation with invalid file extension."""
        mock_file = Mock(spec=UploadFile)
        mock_file.size = 1024
        mock_file.filename = "test.exe"
        mock_file.read = Mock(return_value=b"test content")
        mock_file.seek = Mock()
        
        with pytest.raises(ValidationError) as exc_info:
            await self.file_handler.validate_file(mock_file)
        
        assert "not supported" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_validate_file_empty(self):
        """Test validation with empty file."""
        mock_file = Mock(spec=UploadFile)
        mock_file.size = 1024
        mock_file.filename = "test.pdf"
        mock_file.read = Mock(return_value=b"")
        mock_file.seek = Mock()
        
        with pytest.raises(ValidationError) as exc_info:
            await self.file_handler.validate_file(mock_file)
        
        assert "empty" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_save_file_success(self):
        """Test successful file saving."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Override upload directory for test
            self.file_handler.upload_dir = Path(temp_dir)
            
            # Create mock file
            mock_file = Mock(spec=UploadFile)
            mock_file.filename = "test.pdf"
            mock_file.read = Mock(return_value=b"test content")
            
            job_id = "test-job-123"
            
            # Save file
            file_path = await self.file_handler.save_file(mock_file, job_id)
            
            # Verify file was saved
            assert os.path.exists(file_path)
            assert job_id in file_path
            assert "test.pdf" in file_path
            
            # Verify content
            with open(file_path, 'rb') as f:
                content = f.read()
                assert content == b"test content"
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test dangerous characters
        dangerous_name = "../../../etc/passwd"
        safe_name = self.file_handler._sanitize_filename(dangerous_name)
        assert ".." not in safe_name
        assert "/" not in safe_name
        
        # Test normal filename
        normal_name = "document.pdf"
        safe_name = self.file_handler._sanitize_filename(normal_name)
        assert safe_name == "document.pdf"


class TestJobManager:
    """Test JobManager service."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.job_manager = JobManager()
    
    @pytest.mark.asyncio
    async def test_create_job(self):
        """Test job creation."""
        job_info = await self.job_manager.create_job(
            job_id="test-job-123",
            filename="test.pdf",
            file_path="/tmp/test.pdf",
            file_size=1024,
            options='{"format": "markdown"}'
        )
        
        assert job_info.job_id == "test-job-123"
        assert job_info.filename == "test.pdf"
        assert job_info.file_size == 1024
        assert job_info.status == "pending"
        assert job_info.progress == 0
    
    @pytest.mark.asyncio
    async def test_get_job_status_not_found(self):
        """Test getting status for non-existent job."""
        from app.core.exceptions import NotFoundError
        
        with pytest.raises(NotFoundError):
            await self.job_manager.get_job_status("non-existent-job")
    
    @pytest.mark.asyncio
    async def test_get_job_status_success(self):
        """Test getting status for existing job."""
        # Create job first
        await self.job_manager.create_job(
            job_id="test-job-123",
            filename="test.pdf",
            file_path="/tmp/test.pdf",
            file_size=1024
        )
        
        # Get status
        status = await self.job_manager.get_job_status("test-job-123")
        
        assert status.job_id == "test-job-123"
        assert status.status == "pending"
        assert status.progress == 0
    
    @pytest.mark.asyncio
    async def test_list_jobs_empty(self):
        """Test listing jobs when none exist."""
        job_list = await self.job_manager.list_jobs()
        
        assert job_list.total == 0
        assert len(job_list.jobs) == 0
        assert job_list.page == 1
        assert job_list.per_page == 10
    
    @pytest.mark.asyncio
    async def test_list_jobs_with_data(self):
        """Test listing jobs with data."""
        # Create some jobs
        for i in range(3):
            await self.job_manager.create_job(
                job_id=f"test-job-{i}",
                filename=f"test{i}.pdf",
                file_path=f"/tmp/test{i}.pdf",
                file_size=1024 * (i + 1)
            )
        
        # List jobs
        job_list = await self.job_manager.list_jobs()
        
        assert job_list.total == 3
        assert len(job_list.jobs) == 3
        
        # Check ordering (newest first)
        assert job_list.jobs[0].job_id == "test-job-2"
        assert job_list.jobs[1].job_id == "test-job-1"
        assert job_list.jobs[2].job_id == "test-job-0"
    
    @pytest.mark.asyncio
    async def test_list_jobs_pagination(self):
        """Test job listing pagination."""
        # Create 5 jobs
        for i in range(5):
            await self.job_manager.create_job(
                job_id=f"test-job-{i}",
                filename=f"test{i}.pdf",
                file_path=f"/tmp/test{i}.pdf",
                file_size=1024
            )
        
        # Get first page (2 items)
        job_list = await self.job_manager.list_jobs(page=1, per_page=2)
        
        assert job_list.total == 5
        assert len(job_list.jobs) == 2
        assert job_list.page == 1
        assert job_list.per_page == 2
        
        # Get second page
        job_list = await self.job_manager.list_jobs(page=2, per_page=2)
        
        assert job_list.total == 5
        assert len(job_list.jobs) == 2
        assert job_list.page == 2
