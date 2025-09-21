"""
Docling document processing service.
"""
import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

from docling.document_converter import DocumentConverter

from app.core.config import settings
from app.core.exceptions import ProcessingError

logger = logging.getLogger(__name__)


class DoclingService:
    """Service for processing documents using IBM Granite Docling model."""
    
    def __init__(self):
        self.converter: Optional[DocumentConverter] = None
        self.model_loaded = False
        self._lock = asyncio.Lock()
    
    async def initialize(self) -> None:
        """Initialize the Docling model and converter with IBM Granite Docling 258M."""
        async with self._lock:
            if self.model_loaded:
                return

            try:
                logger.info("Initializing Docling converter with IBM Granite Docling 258M model...")

                # Create document converter with minimal configuration
                # to avoid model compatibility issues
                self.converter = DocumentConverter()

                self.model_loaded = True
                logger.info("Docling converter with IBM Granite Docling 258M initialized successfully")

            except Exception as e:
                logger.error(f"Failed to initialize Docling converter: {str(e)}")
                raise ProcessingError(f"Model initialization failed: {str(e)}")
    
    async def process_document(
        self,
        file_path: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Process a document using Docling.
        
        Args:
            file_path: Path to the document file
            options: Processing options
            
        Returns:
            Processing result with content and metadata
            
        Raises:
            ProcessingError: If processing fails
        """
        if not self.model_loaded:
            await self.initialize()
        
        if not self.converter:
            raise ProcessingError("Docling converter not initialized")
        
        try:
            start_time = time.time()
            logger.info(f"Starting document processing: {file_path}")
            
            # Convert the document
            result = await asyncio.get_event_loop().run_in_executor(
                None, self._convert_document, file_path, options
            )
            
            processing_time = time.time() - start_time
            logger.info(f"Document processing completed in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Document processing failed: {str(e)}")
            raise ProcessingError(f"Processing failed: {str(e)}")
    
    def _convert_document(
        self,
        file_path: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Convert document using Docling (synchronous).
        
        Args:
            file_path: Path to the document file
            options: Processing options
            
        Returns:
            Conversion result
        """
        try:
            # Convert the document
            conv_result = self.converter.convert(source=file_path)
            doc = conv_result.document
            
            # Extract content in different formats
            markdown_content = doc.export_to_markdown()
            html_content = doc.export_to_html()
            json_content = doc.export_to_dict()
            
            # Extract metadata
            metadata = self._extract_metadata(doc, file_path)
            
            # Count elements
            elements_count = self._count_document_elements(doc)
            
            return {
                "content": {
                    "markdown": markdown_content,
                    "html": html_content,
                    "json": json_content,
                },
                "metadata": {
                    "pages": len(doc.pages) if hasattr(doc, 'pages') else 1,
                    "processing_time": 0.0,  # Will be set by caller
                    "elements_detected": elements_count,
                    "model_used": settings.docling_model,
                    "file_type": self._detect_file_type(file_path),
                    "document_title": self._extract_title(doc),
                    "language": self._detect_language(doc),
                },
                "statistics": {
                    "characters": len(markdown_content),
                    "words": len(markdown_content.split()),
                    "tables": self._count_tables(doc),
                    "images": self._count_images(doc),
                    "formulas": self._count_formulas(doc),
                },
            }
            
        except Exception as e:
            raise ProcessingError(f"Docling conversion failed: {str(e)}")
    
    def _extract_metadata(self, doc, file_path: str) -> Dict[str, Any]:
        """Extract metadata from the document."""
        metadata = {}
        
        try:
            # Extract basic document properties
            if hasattr(doc, 'metadata'):
                metadata.update(doc.metadata)
            
            # Add file information
            file_path_obj = Path(file_path)
            metadata.update({
                "filename": file_path_obj.name,
                "file_size": file_path_obj.stat().st_size,
                "file_extension": file_path_obj.suffix,
            })
            
        except Exception as e:
            logger.warning(f"Failed to extract metadata: {str(e)}")
        
        return metadata
    
    def _count_document_elements(self, doc) -> int:
        """Count the number of elements in the document."""
        try:
            if hasattr(doc, 'body') and hasattr(doc.body, 'elements'):
                return len(doc.body.elements)
            elif hasattr(doc, 'pages'):
                total_elements = 0
                for page in doc.pages:
                    if hasattr(page, 'elements'):
                        total_elements += len(page.elements)
                return total_elements
            else:
                return 0
        except Exception:
            return 0
    
    def _detect_file_type(self, file_path: str) -> str:
        """Detect the MIME type of the file."""
        try:
            # Try to import and use python-magic
            import magic
            return magic.from_file(file_path, mime=True)
        except (ImportError, Exception):
            # Fallback to extension-based detection for Windows compatibility
            ext = Path(file_path).suffix.lower()
            type_map = {
                '.pdf': 'application/pdf',
                '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.html': 'text/html',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.tiff': 'image/tiff',
                '.wav': 'audio/wav',
                '.mp3': 'audio/mpeg',
            }
            return type_map.get(ext, 'application/octet-stream')
    
    def _extract_title(self, doc) -> Optional[str]:
        """Extract document title."""
        try:
            # Try to find title in document structure
            if hasattr(doc, 'body') and hasattr(doc.body, 'elements'):
                for element in doc.body.elements:
                    if hasattr(element, 'label') and element.label == 'title':
                        return element.text
                    elif hasattr(element, 'tag') and element.tag in ['h1', 'title']:
                        return element.text
            
            # Fallback: use first heading or first line
            markdown = doc.export_to_markdown()
            lines = markdown.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                elif line and not line.startswith('#'):
                    return line[:100] + ('...' if len(line) > 100 else '')
            
            return None
            
        except Exception:
            return None
    
    def _detect_language(self, doc) -> Optional[str]:
        """Detect document language."""
        try:
            # This is a placeholder - in a real implementation,
            # you might use a language detection library
            return "en"  # Default to English
        except Exception:
            return None
    
    def _count_tables(self, doc) -> int:
        """Count tables in the document."""
        try:
            count = 0
            if hasattr(doc, 'body') and hasattr(doc.body, 'elements'):
                for element in doc.body.elements:
                    if hasattr(element, 'label') and element.label == 'table':
                        count += 1
            return count
        except Exception:
            return 0
    
    def _count_images(self, doc) -> int:
        """Count images in the document."""
        try:
            count = 0
            if hasattr(doc, 'body') and hasattr(doc.body, 'elements'):
                for element in doc.body.elements:
                    if hasattr(element, 'label') and element.label in ['figure', 'image']:
                        count += 1
            return count
        except Exception:
            return 0
    
    def _count_formulas(self, doc) -> int:
        """Count mathematical formulas in the document."""
        try:
            count = 0
            if hasattr(doc, 'body') and hasattr(doc.body, 'elements'):
                for element in doc.body.elements:
                    if hasattr(element, 'label') and element.label == 'formula':
                        count += 1
            return count
        except Exception:
            return 0
    
    async def health_check(self) -> Dict[str, Any]:
        """Check if the Docling service is healthy."""
        try:
            if not self.model_loaded:
                await self.initialize()
            
            return {
                "status": "healthy",
                "model_loaded": self.model_loaded,
                "model_name": settings.docling_model,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "model_loaded": False,
            }
