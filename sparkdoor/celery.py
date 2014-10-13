"""
celery.py - celery web worker configuration module.

    Settings for celery should be put in one of the settings modules,
    not here. This module is just to initialize the celery app.
"""
import os

from celery import Celery

from django.conf import settings


app = Celery('sparkdoor')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
