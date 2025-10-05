"""
WSGI config for prantix project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Automatically detect if running on Azure and use deployment settings
# Check for WEBSITE_HOSTNAME environment variable (set by Azure App Service)
if os.environ.get('WEBSITE_HOSTNAME'):
    settings_module = 'prantix.deployment'
else:
    settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'prantix.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
