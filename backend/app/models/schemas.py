"""
Pydantic models for request/response schemas.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


class ProcessingStatus(str, Enum):
    """Processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class BaseResponse(BaseModel):
    """Base response model."""
    success: bool = True
    message: Optional[str] = None


class ErrorResponse(BaseResponse):
    """Error response model."""
    success: bool = False
    error: str
    code: str
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseResponse):
    """Health check response model."""
    status: str = "healthy"
    version: str
    environment: str


class UploadResponse(BaseResponse):
    """File upload response model."""
    job_id: str = Field(..., description="Unique job identifier")
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    upload_time: datetime = Field(..., description="Upload timestamp")


class StatusResponse(BaseResponse):
    """Processing status response model."""
    job_id: str = Field(..., description="Job identifier")
    status: ProcessingStatus = Field(..., description="Current processing status")
    progress: int = Field(0, ge=0, le=100, description="Progress percentage")
    message: Optional[str] = Field(None, description="Status message")
    started_at: Optional[datetime] = Field(None, description="Processing start time")
    completed_at: Optional[datetime] = Field(None, description="Processing completion time")
    error: Optional[str] = Field(None, description="Error message if failed")


class DocumentMetadata(BaseModel):
    """Document metadata model."""
    pages: int = Field(..., description="Number of pages processed")
    processing_time: float = Field(..., description="Processing time in seconds")
    elements_detected: int = Field(..., description="Number of elements detected")
    model_used: str = Field(..., description="Model used for processing")
    file_size: int = Field(..., description="Original file size in bytes")
    file_type: str = Field(..., description="Original file MIME type")


class ProcessedContent(BaseModel):
    """Processed document content model."""
    markdown: str = Field(..., description="Markdown representation")
    html: str = Field(..., description="HTML representation")
    json_data: Dict[str, Any] = Field(..., alias="json", description="Structured JSON data")


class ResultResponse(BaseResponse):
    """Processing result response model."""
    job_id: str = Field(..., description="Job identifier")
    original_filename: str = Field(..., description="Original filename")
    processed_content: ProcessedContent = Field(..., description="Processed content")
    metadata: DocumentMetadata = Field(..., description="Processing metadata")
    created_at: datetime = Field(..., description="Result creation time")


class JobInfo(BaseModel):
    """Job information model."""
    job_id: str
    filename: str
    status: ProcessingStatus
    created_at: datetime
    updated_at: datetime
    file_size: int
    progress: int = 0
    error: Optional[str] = None


class JobListResponse(BaseResponse):
    """Job list response model."""
    jobs: List[JobInfo] = Field(..., description="List of jobs")
    total: int = Field(..., description="Total number of jobs")
    page: int = Field(1, description="Current page number")
    per_page: int = Field(10, description="Items per page")


# Request models
class ProcessingRequest(BaseModel):
    """Document processing request model."""
    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Processing options"
    )
    
    @validator("options")
    def validate_options(cls, v):
        """Validate processing options."""
        allowed_options = {
            "output_format", "include_images", "extract_tables", 
            "extract_formulas", "ocr_language", "quality"
        }
        if v and not set(v.keys()).issubset(allowed_options):
            invalid_keys = set(v.keys()) - allowed_options
            raise ValueError(f"Invalid options: {invalid_keys}")
        return v
