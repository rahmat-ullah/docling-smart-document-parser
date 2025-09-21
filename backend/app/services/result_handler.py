"""
Result handling service.
"""
import os
import zipfile
import tempfile
from pathlib import Path
from typing import Optional
import markdown

from app.core.config import settings
from app.core.exceptions import NotFoundError


class ResultHandler:
    """Handle processing results and exports."""
    
    def __init__(self):
        self.temp_dir = Path(settings.temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
    
    async def markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert markdown content to HTML.
        
        Args:
            markdown_content: Markdown text
            
        Returns:
            HTML content
        """
        # Convert markdown to HTML with extensions
        html = markdown.markdown(
            markdown_content,
            extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        
        # Wrap in a complete HTML document for preview
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document Preview</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    color: #333;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 1em 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Monaco', 'Consolas', monospace;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                blockquote {{
                    border-left: 4px solid #ddd;
                    margin: 0;
                    padding-left: 20px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        return full_html
    
    async def create_export_archive(
        self,
        job_id: str,
        include_metadata: bool = True,
        include_images: bool = False,
    ) -> str:
        """
        Create a ZIP archive with all processing results.
        
        Args:
            job_id: Job identifier
            include_metadata: Whether to include metadata file
            include_images: Whether to include extracted images
            
        Returns:
            Path to the created ZIP file
            
        Raises:
            NotFoundError: If job or results don't exist
        """
        # This is a placeholder implementation
        # In the real implementation, this would:
        # 1. Get the job result from job_manager
        # 2. Create temporary files for each format
        # 3. Add them to a ZIP archive
        # 4. Include metadata and images if requested
        
        # Create temporary ZIP file
        temp_zip = tempfile.NamedTemporaryFile(
            suffix='.zip',
            dir=self.temp_dir,
            delete=False
        )
        
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add placeholder files (will be replaced with actual content)
            zipf.writestr(f"{job_id}_document.md", "# Sample Document\n\nProcessed content here...")
            zipf.writestr(f"{job_id}_document.html", "<h1>Sample Document</h1><p>Processed content here...</p>")
            zipf.writestr(f"{job_id}_document.json", '{"title": "Sample Document", "content": "Processed content here..."}')
            
            if include_metadata:
                metadata_content = """
                {
                    "job_id": "%s",
                    "processing_time": 4.0,
                    "pages": 1,
                    "elements_detected": 2,
                    "model_used": "granite-docling-258M"
                }
                """ % job_id
                zipf.writestr(f"{job_id}_metadata.json", metadata_content)
            
            if include_images:
                # Placeholder for image files
                zipf.writestr("images/README.txt", "Extracted images would be placed here")
        
        return temp_zip.name
    
    async def cleanup_temp_files(self, older_than_hours: int = 24) -> None:
        """
        Clean up temporary files older than specified hours.
        
        Args:
            older_than_hours: Remove files older than this many hours
        """
        import time
        
        current_time = time.time()
        cutoff_time = current_time - (older_than_hours * 3600)
        
        for file_path in self.temp_dir.iterdir():
            if file_path.is_file():
                try:
                    file_mtime = file_path.stat().st_mtime
                    if file_mtime < cutoff_time:
                        file_path.unlink()
                except Exception:
                    # Ignore errors during cleanup
                    pass
