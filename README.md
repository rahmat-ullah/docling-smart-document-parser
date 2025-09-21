# Docling Document Processing Web Application

A modern web application for document processing using IBM's Granite Docling 258M model. This application provides an intuitive interface for uploading documents and converting them to structured formats with side-by-side comparison views.

## Features

- **Document Upload**: Drag-and-drop file upload with support for PDF, DOCX, PPTX, XLSX, and more
- **Advanced Processing**: Powered by IBM Granite Docling 258M model for accurate document conversion
- **Side-by-Side View**: Compare original documents with processed structured output
- **Real-time Status**: Processing progress indicators and status updates
- **Responsive Design**: Clean, modern UI that works on desktop and mobile devices
- **Error Handling**: Comprehensive error handling for unsupported files and processing failures

## Architecture

### Backend (Python/FastAPI)
- **FastAPI**: High-performance web framework for the API
- **Docling**: IBM's document processing library with Granite Docling 258M model
- **File Handling**: Secure file upload and processing pipeline
- **Error Management**: Robust error handling and logging

### Frontend (React/Vite)
- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **React Query**: Data fetching and state management

## Project Structure

```
docling-app/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend container
├── docker-compose.yml     # Multi-container setup
└── README.md              # This file
```

## Quick Start

### Prerequisites
- **Python 3.9+** (Python 3.11+ recommended for optimal performance)
- **Node.js 18+** with npm
- **Docker** (optional, for containerized deployment)
- **8GB+ RAM** (required for IBM Granite Docling model)
- **10GB+ disk space** (for model downloads and processing)

### Development Setup

> **⚠️ Important**: If you encounter dependency installation errors, please see the [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting steps.

1. **Test dependencies first**
   ```bash
   python test_dependencies.py
   ```

2. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd docling-app
   ```

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   python run_server.py
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Docker Setup

```bash
docker-compose up --build
```

## API Endpoints

- `POST /api/upload` - Upload document for processing
- `GET /api/status/{job_id}` - Check processing status
- `GET /api/result/{job_id}` - Get processed document
- `GET /api/health` - Health check endpoint

## Supported Document Formats

- PDF (.pdf)
- Microsoft Word (.docx)
- Microsoft PowerPoint (.pptx)
- Microsoft Excel (.xlsx)
- HTML (.html)
- Images (PNG, JPEG, TIFF)
- Audio files (WAV, MP3) - with ASR processing

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Docling**: IBM's document processing library
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server
- **Python-multipart**: File upload handling

### Frontend
- **React**: UI library
- **Vite**: Build tool
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **React Query**: Data fetching
- **React Dropzone**: File upload component

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 API Documentation

### Core Endpoints

- **POST /api/upload** - Upload a document for processing
- **GET /api/status/{job_id}** - Get processing status
- **GET /api/result/{job_id}** - Get processing results
- **GET /api/download/{job_id}** - Download processed document
- **GET /api/health** - Health check endpoint

### Supported File Formats

| Format | Extension | Max Size | Notes |
|--------|-----------|----------|-------|
| PDF | `.pdf` | 50MB | Most common document format |
| Word | `.docx` | 50MB | Microsoft Word documents |
| PowerPoint | `.pptx` | 50MB | Presentation files |
| Excel | `.xlsx` | 50MB | Spreadsheet files |
| HTML | `.html` | 50MB | Web pages |
| Images | `.png`, `.jpg`, `.jpeg`, `.tiff` | 50MB | Image documents |
| Audio | `.wav`, `.mp3` | 50MB | Audio files (experimental) |

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
python test_integration.py
```

## 🚀 Deployment

### Production with Docker
```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure sufficient RAM (8GB+ recommended)
   - Check internet connection for model download

2. **File Upload Failures**
   - Check file size limits (50MB max)
   - Verify file format is supported

3. **Frontend Build Issues**
   - Clear node_modules: `rm -rf node_modules && npm install`
   - Check Node.js version (18+ required)

## Acknowledgments

- IBM Research for the Granite Docling model
- The Docling project team for the excellent documentation
- The open-source community for the tools and libraries used
