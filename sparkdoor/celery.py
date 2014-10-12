"""
celery.py - celery web worker configuration module.
"""
import os

from celery import Celery

from django.conf import settings


app = Celery('sparkdoor')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
