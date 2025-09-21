# Docling Application Setup Guide

This guide will help you resolve dependency issues and set up the Docling document processing application successfully.

## 🔧 Dependency Resolution

### Issue Summary
The original `requirements.txt` had several issues:
1. **Incorrect Docling version**: `docling==2.9.2` doesn't exist (latest is `2.53.0`)
2. **Python version compatibility**: Some packages require Python 3.11+
3. **Outdated package versions**: Several dependencies had compatibility issues

### ✅ Fixed Requirements
The updated `requirements.txt` now includes:
- **Docling 2.53.0** (latest stable version)
- **Flexible version ranges** for better compatibility
- **Updated FastAPI and dependencies** to latest stable versions

## 🐍 Python Version Requirements

### Minimum Requirements
- **Python 3.9+** (minimum supported)
- **Python 3.11+** (recommended for optimal performance)
- **8GB+ RAM** (required for IBM Granite Docling model)
- **10GB+ disk space** (for model downloads)

### Check Your Python Version
```bash
python --version
# or
python3 --version
```

If you need to upgrade Python:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew: `brew install python@3.11`
- **Linux**: Use your package manager: `sudo apt install python3.11`

## 📦 Installation Steps

### 1. Test Dependencies First
Before installing, test if your current setup works:
```bash
python test_dependencies.py
```

### 2. Clean Installation (Recommended)
If you have existing issues, start fresh:
```bash
# Remove existing virtual environment
rm -rf venv

# Create new virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Alternative: Upgrade Existing Installation
If you want to keep your current environment:
```bash
# Activate your virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Upgrade pip
python -m pip install --upgrade pip

# Install/upgrade dependencies
pip install -r backend/requirements.txt --upgrade
```

## 🔍 Troubleshooting Common Issues

### Issue 1: "Could not find a version that satisfies the requirement docling==2.9.2"
**Solution**: The requirements.txt has been updated to use `docling==2.53.0`

### Issue 2: Python version compatibility errors
**Solution**: 
- Upgrade to Python 3.11+ for best compatibility
- Or use the flexible version ranges in the updated requirements.txt

### Issue 3: PyTorch installation issues
**Solution**:
```bash
# Install PyTorch separately first
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Then install other requirements
pip install -r backend/requirements.txt
```

### Issue 4: Memory errors during model loading
**Solution**:
- Ensure you have at least 8GB RAM
- Close other applications to free memory
- Consider using CPU-only mode if GPU memory is limited

### Issue 5: "magic" module not found
**Solution**:
```bash
# Windows (recommended)
pip install python-magic-bin

# macOS
brew install libmagic
pip install python-magic

# Linux
sudo apt-get install libmagic1
pip install python-magic
```

### Issue 6: Server startup issues with uvicorn
**Solution**: Use the provided `run_server.py` script instead of direct uvicorn:
```bash
# Instead of: uvicorn app.main:app --reload
# Use:
python run_server.py
```

## 🧪 Verification Steps

### 1. Run Dependency Test
```bash
python test_dependencies.py
```

### 2. Test Backend Startup
```bash
cd backend
uvicorn app.main:app --reload
```

### 3. Test API Endpoints
```bash
# Health check
curl http://localhost:8000/api/health

# API documentation
open http://localhost:8000/docs
```

### 4. Test Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🚀 Quick Start After Setup

Once dependencies are installed successfully:

### 1. Start Backend
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python run_server.py
```

### 2. Start Frontend (new terminal)
```bash
cd frontend
npm run dev
```

### 3. Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🐳 Docker Alternative

If you continue having dependency issues, use Docker:

```bash
# Build and start all services
docker-compose up --build

# Access application at http://localhost:3000
```

## 📋 System Requirements Summary

| Component | Requirement | Recommended |
|-----------|-------------|-------------|
| Python | 3.9+ | 3.11+ |
| RAM | 4GB | 8GB+ |
| Disk Space | 5GB | 10GB+ |
| Node.js | 18+ | 20+ |
| Docker | 20.10+ | Latest |

## 🆘 Getting Help

If you still encounter issues:

1. **Check the logs**: Look for specific error messages
2. **Verify Python version**: Ensure you're using Python 3.9+
3. **Check available memory**: Ensure sufficient RAM for model loading
4. **Try Docker**: Use containerized deployment as fallback
5. **Create an issue**: Report specific error messages with system details

## 📝 Next Steps

After successful setup:
1. Upload a test document through the web interface
2. Monitor processing in the browser console
3. Check the backend logs for any warnings
4. Test different document formats (PDF, DOCX, etc.)

The application should now work correctly with the updated dependencies!
