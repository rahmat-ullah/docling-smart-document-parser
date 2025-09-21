# Deployment Guide

This guide covers different deployment scenarios for the Docling Document Processing Application.

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 8GB+ RAM (for AI model)
- 10GB+ disk space

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd docling-app

# Start all services
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Production Configuration

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DEBUG=false
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    volumes:
      - ./uploads:/app/uploads
      - ./temp:/app/temp
    restart: unless-stopped
    
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - VITE_API_URL=https://your-domain.com/api
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
```

## 🌐 Cloud Deployment

### AWS ECS with Fargate

1. **Build and push images**:
```bash
# Build images
docker build -t docling-backend ./backend
docker build -t docling-frontend ./frontend

# Tag for ECR
docker tag docling-backend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/docling-backend:latest
docker tag docling-frontend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/docling-frontend:latest

# Push to ECR
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/docling-backend:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/docling-frontend:latest
```

2. **Create ECS task definition**:
```json
{
  "family": "docling-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "8192",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/docling-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ]
    }
  ]
}
```

### Google Cloud Run

1. **Deploy backend**:
```bash
gcloud run deploy docling-backend \
  --image gcr.io/PROJECT_ID/docling-backend \
  --platform managed \
  --region us-central1 \
  --memory 8Gi \
  --cpu 2 \
  --max-instances 10
```

2. **Deploy frontend**:
```bash
gcloud run deploy docling-frontend \
  --image gcr.io/PROJECT_ID/docling-frontend \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --cpu 1
```

## 🖥️ Traditional Server Deployment

### Ubuntu/Debian Server

1. **Install dependencies**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+
sudo apt install python3.9 python3.9-venv python3-pip -y

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Nginx
sudo apt install nginx -y

# Install PM2 for process management
sudo npm install -g pm2
```

2. **Deploy backend**:
```bash
# Create application directory
sudo mkdir -p /opt/docling-app
sudo chown $USER:$USER /opt/docling-app
cd /opt/docling-app

# Clone and setup backend
git clone <repository-url> .
cd backend

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/docling-backend.service > /dev/null <<EOF
[Unit]
Description=Docling Backend API
After=network.target

[Service]
Type=exec
User=$USER
WorkingDirectory=/opt/docling-app/backend
Environment=PATH=/opt/docling-app/backend/venv/bin
ExecStart=/opt/docling-app/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable docling-backend
sudo systemctl start docling-backend
```

3. **Deploy frontend**:
```bash
cd /opt/docling-app/frontend

# Install dependencies and build
npm install
npm run build

# Serve with PM2
pm2 serve dist 3000 --name docling-frontend --spa
pm2 startup
pm2 save
```

4. **Configure Nginx**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeout for large file uploads
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # File upload size limit
    client_max_body_size 50M;
}
```

## 🔒 Security Considerations

### SSL/TLS Configuration
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Environment Variables
```bash
# Backend .env
APP_NAME="Docling Document Processing API"
DEBUG=false
ENVIRONMENT=production
SECRET_KEY="your-secret-key-here"
MAX_FILE_SIZE=52428800
ALLOWED_HOSTS=["your-domain.com"]
CORS_ORIGINS=["https://your-domain.com"]

# Database (if using)
DATABASE_URL="postgresql://user:pass@localhost/docling"

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN="your-sentry-dsn"
```

## 📊 Monitoring and Logging

### Health Checks
```bash
# Backend health
curl http://localhost:8000/api/health

# Frontend health
curl http://localhost:3000

# Docker health
docker-compose ps
```

### Log Management
```bash
# View backend logs
sudo journalctl -u docling-backend -f

# View frontend logs
pm2 logs docling-frontend

# Docker logs
docker-compose logs -f backend
```

## 🔧 Maintenance

### Updates
```bash
# Pull latest changes
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart docling-backend

# Update frontend
cd frontend
npm install
npm run build
pm2 restart docling-frontend
```

### Backup
```bash
# Backup uploaded files
tar -czf uploads-backup-$(date +%Y%m%d).tar.gz uploads/

# Backup configuration
cp .env .env.backup
```

## 🚨 Troubleshooting

### Common Issues

1. **Out of Memory**
   - Increase server RAM to 8GB+
   - Configure swap file
   - Reduce `MAX_CONCURRENT_JOBS`

2. **Model Download Fails**
   - Check internet connectivity
   - Verify Hugging Face access
   - Use model cache directory

3. **File Upload Errors**
   - Check Nginx `client_max_body_size`
   - Verify disk space
   - Check file permissions

### Performance Tuning

1. **Backend Optimization**
   - Use Gunicorn with multiple workers
   - Enable GPU acceleration if available
   - Configure Redis for caching

2. **Frontend Optimization**
   - Enable Nginx gzip compression
   - Configure CDN for static assets
   - Implement service worker caching
