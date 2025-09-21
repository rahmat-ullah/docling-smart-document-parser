#!/usr/bin/env python3
"""
Create a simple test PDF document for testing Docling.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

def create_test_pdf():
    """Create a simple test PDF document."""
    
    filename = "test_document.pdf"
    
    # Create a simple PDF using canvas
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Document for Docling")
    
    # Subtitle
    c.setFont("Helvetica", 16)
    c.drawString(100, height - 140, "Document Processing Test")
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 200
    
    content = [
        "This is a test document created for testing the Docling document processing system.",
        "",
        "Key Features to Test:",
        "• Text extraction and processing",
        "• Document structure analysis", 
        "• Content parsing and conversion",
        "• API integration and response handling",
        "",
        "Sample Content:",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod",
        "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim",
        "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea",
        "commodo consequat.",
        "",
        "Technical Details:",
        "- Document format: PDF",
        "- Processing engine: IBM Granite Docling 258M",
        "- Backend: FastAPI with async processing",
        "- Frontend: React with Vite",
        "",
        "This document contains various text elements to test the document",
        "processing capabilities of the Docling system. The system should be",
        "able to extract this text and convert it to a structured format.",
    ]
    
    for line in content:
        c.drawString(100, y_position, line)
        y_position -= 20
        
        # Start new page if needed
        if y_position < 100:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 100
    
    # Save the PDF
    c.save()
    
    print(f"✅ Created test PDF: {filename}")
    print(f"📄 File size: {os.path.getsize(filename)} bytes")
    
    return filename

if __name__ == "__main__":
    create_test_pdf()
