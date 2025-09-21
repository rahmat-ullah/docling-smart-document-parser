"""
Dependency injection for shared services.
"""
from app.services.job_manager import JobManager
from app.services.file_handler import FileHandler
from app.services.docling_service import DoclingService

# Global instances (singletons)
_job_manager = None
_file_handler = None
_docling_service = None


def get_job_manager() -> JobManager:
    """Get the shared JobManager instance."""
    global _job_manager
    if _job_manager is None:
        _job_manager = JobManager()
    return _job_manager


def get_file_handler() -> FileHandler:
    """Get the shared FileHandler instance."""
    global _file_handler
    if _file_handler is None:
        _file_handler = FileHandler()
    return _file_handler


def get_docling_service() -> DoclingService:
    """Get the shared DoclingService instance."""
    global _docling_service
    if _docling_service is None:
        _docling_service = DoclingService()
    return _docling_service
