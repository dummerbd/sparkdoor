"""
wsgi.py - production-specific wsgi configuration module.
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sparkdoor.settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
