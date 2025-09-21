"""
Job management service.
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from app.models.schemas import (
    ProcessingStatus, StatusResponse, ResultResponse,
    JobInfo, JobListResponse, DocumentMetadata, ProcessedContent
)
from app.core.exceptions import NotFoundError, ProcessingError
from app.core.config import settings
from app.services.docling_service import DoclingService

logger = logging.getLogger(__name__)


class JobManager:
    """Manage document processing jobs."""

    def __init__(self):
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.processing_queue = asyncio.Queue(maxsize=settings.max_concurrent_jobs)
        self.active_jobs: Dict[str, asyncio.Task] = {}
        self.docling_service = DoclingService()
    
    async def create_job(
        self,
        job_id: str,
        filename: str,
        file_path: str,
        file_size: int,
        options: Optional[str] = None,
    ) -> JobInfo:
        """
        Create a new processing job.
        
        Args:
            job_id: Unique job identifier
            filename: Original filename
            file_path: Path to uploaded file
            file_size: File size in bytes
            options: Processing options JSON string
            
        Returns:
            Job information
        """
        now = datetime.utcnow()
        
        # Parse options
        parsed_options = {}
        if options:
            try:
                parsed_options = json.loads(options)
            except json.JSONDecodeError:
                pass
        
        # Create job record
        job_data = {
            "job_id": job_id,
            "filename": filename,
            "file_path": file_path,
            "file_size": file_size,
            "status": ProcessingStatus.PENDING,
            "progress": 0,
            "created_at": now,
            "updated_at": now,
            "options": parsed_options,
            "error": None,
            "result": None,
        }
        
        self.jobs[job_id] = job_data
        logger.info(f"Created job {job_id}. Total jobs: {len(self.jobs)}")

        return JobInfo(
            job_id=job_id,
            filename=filename,
            status=ProcessingStatus.PENDING,
            created_at=now,
            updated_at=now,
            file_size=file_size,
            progress=0,
        )
    
    async def get_job_status(self, job_id: str) -> StatusResponse:
        """
        Get the current status of a job.

        Args:
            job_id: Job identifier

        Returns:
            Current job status

        Raises:
            NotFoundError: If job doesn't exist
        """
        logger.debug(f"Looking for job {job_id}. Available jobs: {list(self.jobs.keys())}")

        if job_id not in self.jobs:
            logger.warning(f"Job {job_id} not found. Available jobs: {list(self.jobs.keys())}")
            raise NotFoundError(f"Job {job_id} not found")

        job = self.jobs[job_id]
        logger.debug(f"Found job {job_id} with status: {job['status']}")
        
        return StatusResponse(
            job_id=job_id,
            status=job["status"],
            progress=job["progress"],
            message=job.get("message"),
            started_at=job.get("started_at"),
            completed_at=job.get("completed_at"),
            error=job.get("error"),
        )
    
    async def get_job_result(self, job_id: str) -> ResultResponse:
        """
        Get the processing result for a completed job.
        
        Args:
            job_id: Job identifier
            
        Returns:
            Processing result
            
        Raises:
            NotFoundError: If job doesn't exist or isn't completed
        """
        if job_id not in self.jobs:
            raise NotFoundError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        
        if job["status"] != ProcessingStatus.COMPLETED:
            raise NotFoundError(f"Job {job_id} is not completed")
        
        if not job.get("result"):
            raise NotFoundError(f"No result available for job {job_id}")
        
        result = job["result"]
        
        return ResultResponse(
            job_id=job_id,
            original_filename=job["filename"],
            processed_content=ProcessedContent(
                markdown=result["content"]["markdown"],
                html=result["content"]["html"],
                json=result["content"]["json"],
            ),
            metadata=DocumentMetadata(
                pages=result["metadata"]["pages"],
                processing_time=result["metadata"]["processing_time"],
                elements_detected=result["metadata"]["elements_detected"],
                model_used=result["metadata"]["model_used"],
                file_size=job["file_size"],
                file_type=result["metadata"]["file_type"],
            ),
            created_at=job["completed_at"],
        )
    
    async def list_jobs(
        self,
        page: int = 1,
        per_page: int = 10,
        status_filter: Optional[str] = None,
    ) -> JobListResponse:
        """
        List jobs with pagination and filtering.
        
        Args:
            page: Page number
            per_page: Items per page
            status_filter: Optional status filter
            
        Returns:
            Paginated job list
        """
        # Filter jobs
        filtered_jobs = []
        for job in self.jobs.values():
            if status_filter and job["status"] != status_filter:
                continue
            filtered_jobs.append(job)
        
        # Sort by creation time (newest first)
        filtered_jobs.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Paginate
        total = len(filtered_jobs)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_jobs = filtered_jobs[start_idx:end_idx]
        
        # Convert to JobInfo objects
        job_infos = [
            JobInfo(
                job_id=job["job_id"],
                filename=job["filename"],
                status=job["status"],
                created_at=job["created_at"],
                updated_at=job["updated_at"],
                file_size=job["file_size"],
                progress=job["progress"],
                error=job.get("error"),
            )
            for job in page_jobs
        ]
        
        return JobListResponse(
            jobs=job_infos,
            total=total,
            page=page,
            per_page=per_page,
        )
    
    async def process_document(
        self,
        job_id: str,
        file_path: str,
        options: Optional[str] = None,
    ) -> None:
        """
        Process a document using Docling.

        Args:
            job_id: Job identifier
            file_path: Path to the file to process
            options: Processing options
        """
        if job_id not in self.jobs:
            logger.warning(f"Job {job_id} not found, skipping processing")
            return

        job = self.jobs[job_id]
        start_time = datetime.utcnow()

        try:
            logger.info(f"Starting processing for job {job_id}: {job['filename']}")

            # Update status to processing
            job["status"] = ProcessingStatus.PROCESSING
            job["started_at"] = start_time
            job["progress"] = 10
            job["updated_at"] = datetime.utcnow()

            # Parse processing options
            parsed_options = {}
            if options:
                try:
                    parsed_options = json.loads(options)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid options JSON for job {job_id}: {options}")

            # Initialize Docling service if needed
            job["progress"] = 20
            job["updated_at"] = datetime.utcnow()

            # Process document with Docling
            job["progress"] = 30
            job["updated_at"] = datetime.utcnow()

            result = await self.docling_service.process_document(
                file_path=file_path,
                options=parsed_options
            )

            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            result["metadata"]["processing_time"] = processing_time

            # Update job with result
            job["status"] = ProcessingStatus.COMPLETED
            job["progress"] = 100
            job["completed_at"] = datetime.utcnow()
            job["result"] = result

            logger.info(f"Successfully processed job {job_id} in {processing_time:.2f}s")

        except Exception as e:
            # Handle processing error
            logger.error(f"Processing failed for job {job_id}: {str(e)}", exc_info=True)
            job["status"] = ProcessingStatus.FAILED
            job["error"] = str(e)
            job["completed_at"] = datetime.utcnow()

        finally:
            job["updated_at"] = datetime.utcnow()
            # Remove from active jobs if present
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
    
    async def cancel_job(self, job_id: str) -> None:
        """Cancel a running job."""
        if job_id not in self.jobs:
            raise NotFoundError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        
        if job["status"] in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED]:
            raise ProcessingError("Cannot cancel completed or failed job")
        
        # Cancel the task if it's running
        if job_id in self.active_jobs:
            self.active_jobs[job_id].cancel()
            del self.active_jobs[job_id]
        
        # Update job status
        job["status"] = ProcessingStatus.FAILED
        job["error"] = "Job cancelled by user"
        job["completed_at"] = datetime.utcnow()
        job["updated_at"] = datetime.utcnow()
    
    async def retry_job(self, job_id: str) -> None:
        """Retry a failed job."""
        if job_id not in self.jobs:
            raise NotFoundError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        
        if job["status"] != ProcessingStatus.FAILED:
            raise ProcessingError("Can only retry failed jobs")
        
        # Reset job status
        job["status"] = ProcessingStatus.PENDING
        job["progress"] = 0
        job["error"] = None
        job["updated_at"] = datetime.utcnow()
        
        # Restart processing
        await self.process_document(job_id, job["file_path"], json.dumps(job["options"]))
