"""
WSGI config for prantix project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = 'prantix.deployment' if os.environ.get('WEBSITE_HOSTNAME') else 'prantix.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prantix.settings')

application = get_wsgi_application()
