"""
Results and download endpoints.
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse, FileResponse
from typing import Optional
import os
import json

from app.models.schemas import ResultResponse
from app.core.exceptions import NotFoundError
from app.core.dependencies import get_job_manager
from app.services.result_handler import ResultHandler

router = APIRouter()
result_handler = ResultHandler()


@router.get("/result/{job_id}", response_model=ResultResponse)
async def get_result(job_id: str):
    """
    Get the processing result for a completed job.
    
    Args:
        job_id: The unique job identifier
    
    Returns:
        Complete processing result with content and metadata
    """
    try:
        job_manager = get_job_manager()
        result = await job_manager.get_job_result(job_id)
        return result
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get result: {str(e)}")


@router.get("/download/{job_id}")
async def download_result(
    job_id: str,
    format: str = Query("markdown", regex="^(markdown|html|json)$"),
):
    """
    Download the processed document in the specified format.
    
    Args:
        job_id: The unique job identifier
        format: Output format (markdown, html, or json)
    
    Returns:
        File download response
    """
    try:
        # Get the result
        job_manager = get_job_manager()
        result = await job_manager.get_job_result(job_id)
        
        # Generate filename
        base_name = os.path.splitext(result.original_filename)[0]
        
        if format == "markdown":
            content = result.processed_content.markdown
            filename = f"{base_name}.md"
            media_type = "text/markdown"
        elif format == "html":
            content = result.processed_content.html
            filename = f"{base_name}.html"
            media_type = "text/html"
        elif format == "json":
            content = json.dumps(result.processed_content.json_data, indent=2)
            filename = f"{base_name}.json"
            media_type = "application/json"
        else:
            raise HTTPException(status_code=400, detail="Invalid format")
        
        # Create streaming response
        def generate():
            yield content.encode('utf-8')
        
        return StreamingResponse(
            generate(),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download: {str(e)}")


@router.get("/preview/{job_id}")
async def preview_result(
    job_id: str,
    format: str = Query("html", regex="^(html|markdown)$"),
):
    """
    Preview the processed document in the browser.
    
    Args:
        job_id: The unique job identifier
        format: Preview format (html or markdown)
    
    Returns:
        HTML content for browser preview
    """
    try:
        job_manager = get_job_manager()
        result = await job_manager.get_job_result(job_id)
        
        if format == "html":
            content = result.processed_content.html
            media_type = "text/html"
        elif format == "markdown":
            # Convert markdown to HTML for preview
            content = await result_handler.markdown_to_html(
                result.processed_content.markdown
            )
            media_type = "text/html"
        else:
            raise HTTPException(status_code=400, detail="Invalid format")
        
        return StreamingResponse(
            iter([content.encode('utf-8')]),
            media_type=media_type
        )
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to preview: {str(e)}")


@router.get("/export/{job_id}")
async def export_result(
    job_id: str,
    include_metadata: bool = Query(True, description="Include processing metadata"),
    include_images: bool = Query(False, description="Include extracted images"),
):
    """
    Export complete processing result as a ZIP archive.
    
    Args:
        job_id: The unique job identifier
        include_metadata: Whether to include metadata file
        include_images: Whether to include extracted images
    
    Returns:
        ZIP file download
    """
    try:
        zip_path = await result_handler.create_export_archive(
            job_id=job_id,
            include_metadata=include_metadata,
            include_images=include_images,
        )
        
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename=f"docling_export_{job_id}.zip"
        )
        
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export: {str(e)}")
