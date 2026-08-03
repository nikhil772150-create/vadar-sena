from .base import *
import os

DEBUG = False

# Production Allowed Hosts - allow all hosts (Render domains, custom domain bhartiyavadar.com, localhost)
ALLOWED_HOSTS = ['*']

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

# CORS Configuration for Production
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

SECRET_KEY = os.getenv('SECRET_KEY', 'bvsms-prod-secure-key-bhartiyavadar-2026')

# Production Security Controls
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static & Media Files Production Root
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
