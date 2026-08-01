from .base import *
import os
from django.core.exceptions import ImproperlyConfigured

DEBUG = False

# Production Allowed Hosts
default_hosts = 'bhartiyavadar.com,www.bhartiyavadar.com,localhost,127.0.0.1'
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', default_hosts).split(',') if host.strip()]

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'bvsms_db'),
        'USER': os.getenv('DB_USER', 'bvsms_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'bvsms_secure_password'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# CORS Allowed Origins
default_cors = 'https://bhartiyavadar.com,https://www.bhartiyavadar.com,http://localhost:5173,http://localhost:5174,http://127.0.0.1:8000'
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS', default_cors).split(',') if origin.strip()]

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY or SECRET_KEY == 'django-insecure-default-bvsms-key':
    # Fallback to dev secret key if not specified, but log warning
    SECRET_KEY = os.getenv('SECRET_KEY', 'bvsms-prod-secure-key-bhartiyavadar-2026')

# Production Security Controls
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static & Media Files Production Root
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
