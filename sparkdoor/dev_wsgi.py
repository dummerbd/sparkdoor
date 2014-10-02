"""
dev_wsgi.py - development-specific wsgi configuration module.
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sparkdoor.settings.development")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
