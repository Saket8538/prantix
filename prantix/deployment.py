import os
from .settings import *
from .settings import BASE_DIR

# CRITICAL: Use .get() with defaults to prevent crashes on missing env vars
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', os.environ.get('SECRET_KEY', 'CHANGE-ME-IN-PRODUCTION'))
WEBSITE_HOSTNAME = os.environ.get('WEBSITE_HOSTNAME', 'localhost')

# Allow both with and without wildcard
ALLOWED_HOSTS = [WEBSITE_HOSTNAME]
if WEBSITE_HOSTNAME != 'localhost':
    ALLOWED_HOSTS.extend([f".{WEBSITE_HOSTNAME}", '*.azurewebsites.net'])

CSRF_TRUSTED_ORIGINS = [f"https://{WEBSITE_HOSTNAME}"]
if WEBSITE_HOSTNAME != 'localhost':
    CSRF_TRUSTED_ORIGINS.append(f"https://*.azurewebsites.net")

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database Configuration for Azure PostgreSQL Flexible Server
# Use Managed Identity for secure authentication (recommended)
# Connection strings are automatically injected by Azure App Service
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DBNAME', 'prantix_db'),
        'HOST': os.environ.get('DBHOST', ''),
        'USER': os.environ.get('DBUSER', ''),
        'PASSWORD': os.environ.get('DBPASS', ''),
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL for security
        },
    }
}

# Static and Media Files Configuration
# Django 4.2+ uses STORAGES instead of STATICFILES_STORAGE
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files - IMPORTANT: Use Azure Blob Storage for production
# For now, local storage works but consider Azure Blob Storage for scalability
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'