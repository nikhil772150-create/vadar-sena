from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': BASE_DIR / 'db.sqlite3' if os.getenv('DB_ENGINE', 'sqlite3') == 'sqlite3' else os.getenv('DB_NAME', 'bvsms_db'),
    }
}

# Local CORS
CORS_ALLOW_ALL_ORIGINS = True
