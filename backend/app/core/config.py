"""
Application configuration settings.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Docling Document Processing API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # API
    api_prefix: str = "/api"
    allowed_hosts: List[str] = ["*"]
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    
    # File handling
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    upload_dir: str = "uploads"
    temp_dir: str = "temp"
    allowed_extensions: List[str] = [
        ".pdf", ".docx", ".pptx", ".xlsx", 
        ".html", ".png", ".jpg", ".jpeg", 
        ".tiff", ".wav", ".mp3"
    ]
    
    # Docling settings
    docling_model: str = "ibm-granite/granite-docling-258M"
    docling_device: str = "auto"  # auto, cpu, cuda, mps
    docling_batch_size: int = 1
    
    # Processing
    max_concurrent_jobs: int = 5
    job_timeout: int = 300  # 5 minutes
    cleanup_interval: int = 3600  # 1 hour
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    @validator("upload_dir", "temp_dir")
    def create_directories(cls, v):
        """Create directories if they don't exist."""
        os.makedirs(v, exist_ok=True)
        return v
    
    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from environment variable."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
