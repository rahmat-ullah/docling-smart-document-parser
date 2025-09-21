"""
File handling service.
"""
import os
import aiofiles
# import magic  # Commented out for Windows compatibility
from typing import Optional
from pathlib import Path
from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import FileError, ValidationError


class FileHandler:
    """Handle file operations and validation."""
    
    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.temp_dir = Path(settings.temp_dir)
        
        # Ensure directories exist
        self.upload_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    async def validate_file(self, file: UploadFile) -> None:
        """
        Validate uploaded file.
        
        Args:
            file: The uploaded file to validate
            
        Raises:
            ValidationError: If file validation fails
        """
        # Check file size
        if file.size > settings.max_file_size:
            raise ValidationError(
                f"File size ({file.size} bytes) exceeds maximum allowed size "
                f"({settings.max_file_size} bytes)"
            )
        
        # Check filename
        if not file.filename:
            raise ValidationError("Filename is required")
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in settings.allowed_extensions:
            raise ValidationError(
                f"File extension '{file_ext}' is not supported. "
                f"Allowed extensions: {', '.join(settings.allowed_extensions)}"
            )
        
        # Read a small chunk to validate file content
        chunk = await file.read(1024)
        await file.seek(0)  # Reset file pointer
        
        if not chunk:
            raise ValidationError("File appears to be empty")
        
        # Validate MIME type using python-magic
        try:
            # Try to import and use python-magic
            import magic
            mime_type = magic.from_buffer(chunk, mime=True)
            if not self._is_mime_type_allowed(mime_type, file_ext):
                raise ValidationError(
                    f"File content type '{mime_type}' does not match extension '{file_ext}'"
                )
        except (ImportError, Exception) as e:
            # If magic fails, we'll rely on extension validation
            pass
    
    def _is_mime_type_allowed(self, mime_type: str, file_ext: str) -> bool:
        """Check if MIME type matches the file extension."""
        allowed_mime_types = {
            '.pdf': ['application/pdf'],
            '.docx': [
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/zip'  # DOCX files are ZIP archives
            ],
            '.pptx': [
                'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'application/zip'
            ],
            '.xlsx': [
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/zip'
            ],
            '.html': ['text/html', 'text/plain'],
            '.png': ['image/png'],
            '.jpg': ['image/jpeg'],
            '.jpeg': ['image/jpeg'],
            '.tiff': ['image/tiff'],
            '.wav': ['audio/wav', 'audio/x-wav'],
            '.mp3': ['audio/mpeg', 'audio/mp3'],
        }
        
        return mime_type in allowed_mime_types.get(file_ext, [])
    
    async def save_file(self, file: UploadFile, job_id: str) -> str:
        """
        Save uploaded file to disk.
        
        Args:
            file: The uploaded file
            job_id: Unique job identifier
            
        Returns:
            Path to the saved file
            
        Raises:
            FileError: If file saving fails
        """
        try:
            # Create job-specific directory
            job_dir = self.upload_dir / job_id
            job_dir.mkdir(exist_ok=True)
            
            # Generate safe filename
            safe_filename = self._sanitize_filename(file.filename)
            file_path = job_dir / safe_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            return str(file_path)
            
        except Exception as e:
            raise FileError(f"Failed to save file: {str(e)}")
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal attacks."""
        # Remove path components and keep only the filename
        filename = os.path.basename(filename)
        
        # Replace potentially dangerous characters
        dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        return filename
    
    async def delete_file(self, file_path: str) -> None:
        """
        Delete a file from disk.
        
        Args:
            file_path: Path to the file to delete
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            # Log error but don't raise - file cleanup is not critical
            pass
    
    async def cleanup_job_files(self, job_id: str) -> None:
        """
        Clean up all files associated with a job.
        
        Args:
            job_id: Job identifier
        """
        try:
            job_dir = self.upload_dir / job_id
            if job_dir.exists():
                # Remove all files in the job directory
                for file_path in job_dir.iterdir():
                    if file_path.is_file():
                        file_path.unlink()
                # Remove the directory
                job_dir.rmdir()
        except Exception:
            # Log error but don't raise
            pass
