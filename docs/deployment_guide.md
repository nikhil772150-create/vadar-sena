# Production Deployment Guide — Bharatiya Vadar Sena Management System (BVSMS)

## Overview
This document outlines the step-by-step production deployment procedures for BVSMS across Docker Compose, PostgreSQL 15, Django 5 Gunicorn, and Nginx.

---

## 1. Prerequisites
- Linux Server (Ubuntu 22.04 LTS recommended, 4GB+ RAM, 2 vCPUs)
- Docker Engine v24+ & Docker Compose v2+
- Domain Name with SSL Certificate (Certbot / Let's Encrypt)

---

## 2. Production Environment Configuration

Create a `.env` file in the root workspace:

```env
# General Settings
DEBUG=False
SECRET_KEY=generate-a-strong-50-character-secret-key-here
ALLOWED_HOSTS=bvsms.org,www.bvsms.org,api.bvsms.org

# Database Configuration
POSTGRES_DB=bvsms_prod_db
POSTGRES_USER=bvsms_admin
POSTGRES_PASSWORD=use-a-strong-postgres-password
DB_HOST=db
DB_PORT=5432

# CORS & Trusted Origins
CORS_ALLOWED_ORIGINS=https://bvsms.org,https://www.bvsms.org
CSRF_TRUSTED_ORIGINS=https://bvsms.org,https://api.bvsms.org
```

---

## 3. Docker Container Deployment

Execute the following commands on the target host server:

```bash
# Clone production repository
git clone https://github.com/vadarsena/bvsms.git
cd bvsms

# Build and launch multi-container stack in detached mode
docker-compose -f docker-compose.yml up -d --build

# Execute database migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Create SuperAdmin User
docker-compose exec backend python manage.py createsuperuser
```

---

## 4. Nginx & SSL Configuration

Verify Nginx reverse proxy configuration (`docker/nginx/nginx.conf`):

```nginx
server {
    listen 80;
    server_name bvsms.org www.bvsms.org;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name bvsms.org www.bvsms.org;

    ssl_certificate /etc/letsencrypt/live/bvsms.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bvsms.org/privkey.pem;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

---

## 5. System Health Check & Verification

Validate running services:

```bash
# Check container status
docker-compose ps

# Query System Health API
curl -i https://bvsms.org/api/v1/health/
# Expected HTTP 200 OK: {"status": "healthy", "database": "connected"}
```
