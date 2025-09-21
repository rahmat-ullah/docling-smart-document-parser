"""
Custom exception classes.
"""
from typing import Optional, Any


class AppException(Exception):
    """Base application exception."""
    
    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = 400,
        details: Optional[Any] = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ValidationError(AppException):
    """Validation error exception."""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class FileError(AppException):
    """File handling error exception."""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="FILE_ERROR",
            status_code=400,
            details=details,
        )


class ProcessingError(AppException):
    """Document processing error exception."""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="PROCESSING_ERROR",
            status_code=500,
            details=details,
        )


class NotFoundError(AppException):
    """Resource not found exception."""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details=details,
        )


class RateLimitError(AppException):
    """Rate limit exceeded exception."""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Any] = None):
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details=details,
        )
