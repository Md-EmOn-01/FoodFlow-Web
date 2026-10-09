"""
WSGI config for FoodFlow project.
Exposes the WSGI callable as a module-level variable named ``application`` and ``app`` (for Vercel).
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Vercel serverless entrypoint
app = application
