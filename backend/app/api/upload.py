"""
File upload endpoints.
"""
import os
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import aiofiles
# import magic  # Commented out for Windows compatibility

from app.models.schemas import UploadResponse, ErrorResponse
from app.core.config import settings
from app.core.exceptions import FileError, ValidationError
from app.core.dependencies import get_file_handler, get_job_manager

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    options: Optional[str] = None,
):
    """
    Upload a document for processing.
    
    Args:
        file: The document file to upload
        options: Optional processing options (JSON string)
    
    Returns:
        Upload response with job ID and file information
    """
    try:
        # Get shared instances
        file_handler = get_file_handler()
        job_manager = get_job_manager()

        # Validate file
        await file_handler.validate_file(file)

        # Generate job ID
        job_id = str(uuid.uuid4())

        # Save file
        file_path = await file_handler.save_file(file, job_id)

        # Create job record
        job_info = await job_manager.create_job(
            job_id=job_id,
            filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            options=options,
        )
        
        # Start background processing
        background_tasks.add_task(
            job_manager.process_document,
            job_id,
            file_path,
            options
        )
        
        return UploadResponse(
            job_id=job_id,
            filename=file.filename,
            file_size=file.size,
            upload_time=datetime.utcnow(),
        )
        
    except (FileError, ValidationError) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/upload/limits")
async def get_upload_limits():
    """
    Get upload limits and supported file types.
    
    Returns:
        Information about upload constraints
    """
    return {
        "success": True,
        "limits": {
            "max_file_size": settings.max_file_size,
            "max_file_size_mb": settings.max_file_size // (1024 * 1024),
            "allowed_extensions": settings.allowed_extensions,
            "max_concurrent_jobs": settings.max_concurrent_jobs,
        },
        "supported_formats": {
            "documents": [".pdf", ".docx", ".pptx", ".xlsx", ".html"],
            "images": [".png", ".jpg", ".jpeg", ".tiff"],
            "audio": [".wav", ".mp3"],
        }
    }
