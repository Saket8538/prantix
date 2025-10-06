import os
import re
from .settings import *
from .settings import BASE_DIR

# CRITICAL: Use .get() with defaults to prevent crashes on missing env vars
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', os.environ.get('SECRET_KEY', 'CHANGE-ME-IN-PRODUCTION'))

# WEBSITE_HOSTNAME is automatically set by Azure App Service (read-only system variable)
# DO NOT manually create WEBSITE_HOSTNAME in App Settings - Azure provides it automatically
WEBSITE_HOSTNAME = os.environ.get('WEBSITE_HOSTNAME', '')

# Use ALLOWED_HOSTS from App Settings (you already set this correctly)
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '')

# Parse ALLOWED_HOSTS from Azure (can be comma-separated or single value)
if allowed_hosts_env:
    # User explicitly set ALLOWED_HOSTS in Azure App Settings
    if ',' in allowed_hosts_env:
        ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',')]
    else:
        ALLOWED_HOSTS = [allowed_hosts_env.strip()]
    # Add wildcard support for Azure
    ALLOWED_HOSTS.extend(['*.azurewebsites.net'])
    primary_host = allowed_hosts_env.split(',')[0].strip() if ',' in allowed_hosts_env else allowed_hosts_env.strip()
elif WEBSITE_HOSTNAME:
    # Fallback to WEBSITE_HOSTNAME if ALLOWED_HOSTS not set (Azure auto-provides this)
    ALLOWED_HOSTS = [WEBSITE_HOSTNAME, f".{WEBSITE_HOSTNAME}", '*.azurewebsites.net']
    primary_host = WEBSITE_HOSTNAME
else:
    # Development/local fallback
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    primary_host = 'localhost'

# CSRF trusted origins based on detected hostname
if primary_host and primary_host != 'localhost':
    CSRF_TRUSTED_ORIGINS = [f"https://{primary_host}", "https://*.azurewebsites.net"]
else:
    CSRF_TRUSTED_ORIGINS = []

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

# Security settings for production
# CRITICAL: Do NOT set SECURE_SSL_REDIRECT=True on Azure App Service!
# Azure terminates SSL at the load balancer, causing infinite redirect loops
# Azure handles HTTPS automatically - the app receives HTTP from the load balancer
SECURE_SSL_REDIRECT = False  # Azure handles SSL termination
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Azure-specific: Trust the X-Forwarded-Proto header from Azure's load balancer
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
# Azure provides connection string in AZURE_POSTGRESQL_CONNECTIONSTRING
# Parse it or use individual env vars (DBNAME, DBHOST, DBUSER, DBPASS)

# Try to parse Azure connection string first
azure_db_connection = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING', '')

if azure_db_connection:
    # Parse Azure connection string format:
    # "dbname=xxx host=xxx.postgres.database.azure.com port=5432 sslmode=require user=xxx password=xxx"
    db_config = {}
    for pair in azure_db_connection.split():
        if '=' in pair:
            key, value = pair.split('=', 1)
            db_config[key] = value
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_config.get('dbname', 'prantix_db'),
            'HOST': db_config.get('host', ''),
            'USER': db_config.get('user', ''),
            'PASSWORD': db_config.get('password', ''),
            'PORT': db_config.get('port', '5432'),
            'OPTIONS': {
                'sslmode': db_config.get('sslmode', 'require'),
            },
        }
    }
else:
    # Fallback to individual environment variables
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