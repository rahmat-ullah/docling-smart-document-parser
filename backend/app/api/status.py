"""
Job status endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.schemas import StatusResponse, JobListResponse
from app.core.exceptions import NotFoundError
from app.core.dependencies import get_job_manager

router = APIRouter()


@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_job_status(job_id: str):
    """
    Get the processing status of a specific job.

    Args:
        job_id: The unique job identifier

    Returns:
        Current status and progress information
    """
    try:
        job_manager = get_job_manager()
        status = await job_manager.get_job_status(job_id)
        return status
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
):
    """
    List all jobs with optional filtering.
    
    Args:
        page: Page number for pagination
        per_page: Number of items per page
        status: Optional status filter
    
    Returns:
        List of jobs with pagination information
    """
    try:
        job_manager = get_job_manager()
        jobs = await job_manager.list_jobs(
            page=page,
            per_page=per_page,
            status_filter=status,
        )
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list jobs: {str(e)}")


@router.delete("/jobs/{job_id}")
async def cancel_job(job_id: str):
    """
    Cancel a running job.
    
    Args:
        job_id: The unique job identifier
    
    Returns:
        Cancellation confirmation
    """
    try:
        job_manager = get_job_manager()
        await job_manager.cancel_job(job_id)
        return {
            "success": True,
            "message": f"Job {job_id} has been cancelled",
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel job: {str(e)}")


@router.post("/jobs/{job_id}/retry")
async def retry_job(job_id: str):
    """
    Retry a failed job.
    
    Args:
        job_id: The unique job identifier
    
    Returns:
        Retry confirmation
    """
    try:
        job_manager = get_job_manager()
        await job_manager.retry_job(job_id)
        return {
            "success": True,
            "message": f"Job {job_id} has been queued for retry",
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retry job: {str(e)}")
