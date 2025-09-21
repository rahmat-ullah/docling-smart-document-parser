# Contributing to Docling Document Processing Application

Thank you for your interest in contributing to the Docling Document Processing Application! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.9+** (Python 3.11+ recommended)
- **Node.js 18+** with npm
- **Git** for version control
- **8GB+ RAM** (required for IBM Granite Docling model)
- **10GB+ disk space** (for model downloads and processing)

### Development Environment Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/rahmat-ullah/docling-smart-document-parser.git
   cd docling-smart-document-parser
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Test the Setup**
   ```bash
   # Test backend
   cd backend
   python run_server.py

   # Test frontend (in a new terminal)
   cd frontend
   npm run dev
   ```

## 📋 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the coding standards outlined below
- Write tests for new functionality
- Update documentation as needed
- Ensure your changes don't break existing functionality

### 3. Test Your Changes

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# Integration tests
python test_integration.py
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 🎯 Coding Standards

### Python (Backend)

- **Code Style**: Follow PEP 8 guidelines
- **Formatting**: Use `black` for code formatting
- **Import Sorting**: Use `isort` for import organization
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Use Google-style docstrings for all functions and classes

```python
def process_document(file_path: str, options: Dict[str, Any]) -> ProcessingResult:
    """
    Process a document using the Docling model.
    
    Args:
        file_path: Path to the document file
        options: Processing options dictionary
        
    Returns:
        ProcessingResult containing the processed document data
        
    Raises:
        ProcessingError: If document processing fails
    """
    pass
```

- **Error Handling**: Use custom exceptions and proper error logging
- **Async/Await**: Use async/await for I/O operations
- **Testing**: Write unit tests with pytest

### TypeScript/React (Frontend)

- **Code Style**: Follow TypeScript and React best practices
- **Formatting**: Use Prettier for code formatting
- **Components**: Use functional components with hooks
- **Type Safety**: Define interfaces for all props and state
- **File Naming**: Use PascalCase for components, camelCase for utilities

```typescript
interface DocumentUploadProps {
  onUpload: (file: File) => void;
  maxSize?: number;
  acceptedTypes?: string[];
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUpload,
  maxSize = 50 * 1024 * 1024, // 50MB
  acceptedTypes = ['application/pdf']
}) => {
  // Component implementation
};
```

### Code Quality Tools

Run these tools before submitting:

```bash
# Backend
cd backend
black .
isort .
flake8 .
mypy .

# Frontend
cd frontend
npm run lint
npm run type-check
```

## 🧪 Testing Guidelines

### Backend Testing

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and service interactions
- **Test Coverage**: Aim for >80% test coverage
- **Test Files**: Place tests in `backend/tests/` directory

```python
import pytest
from app.services.docling_service import DoclingService

@pytest.mark.asyncio
async def test_document_processing():
    service = DoclingService()
    result = await service.process_document("test.pdf")
    assert result is not None
    assert "content" in result
```

### Frontend Testing

- **Component Tests**: Test React components with React Testing Library
- **Integration Tests**: Test user interactions and API calls
- **Type Checking**: Ensure TypeScript compilation passes

## 📝 Documentation

### Code Documentation

- **Python**: Use Google-style docstrings
- **TypeScript**: Use JSDoc comments for complex functions
- **README Updates**: Update README.md for new features
- **API Documentation**: Update OpenAPI/Swagger documentation

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(api): add document batch processing endpoint`
- `fix(frontend): resolve file upload progress indicator`
- `docs(readme): update installation instructions`

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Operating system and version
   - Python version
   - Node.js version
   - Browser (for frontend issues)

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Screenshots if applicable

3. **Error Messages**
   - Full error messages and stack traces
   - Console logs (for frontend issues)

4. **Additional Context**
   - File types being processed
   - File sizes
   - Any relevant configuration

## 💡 Feature Requests

For feature requests, please:

1. **Check Existing Issues**: Search for similar requests
2. **Provide Context**: Explain the use case and problem
3. **Suggest Implementation**: If you have ideas for implementation
4. **Consider Scope**: Keep requests focused and well-defined

## 🔒 Security

- **Security Issues**: Report security vulnerabilities privately via email
- **Dependencies**: Keep dependencies updated and secure
- **Input Validation**: Validate all user inputs
- **File Handling**: Implement secure file upload and processing

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check existing documentation first

## 🎉 Recognition

Contributors will be recognized in:
- CHANGELOG.md for their contributions
- GitHub contributors list
- Special mentions for significant contributions

Thank you for contributing to the Docling Document Processing Application!
