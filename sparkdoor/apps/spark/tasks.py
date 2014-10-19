"""
tasks.py - `spark` app web worker tasks module.
"""
from celery import shared_task

from .models import CloudCredentials


@shared_task
def refresh_access_token():
    """
    Run this task periodically to check for soon to expire access tokens
    and request a new one when needed. This task can also be run on
    demand in the case that an access token is expired.
    """
    token = CloudCredentials.objects.access_token()
    if token is None:
        token = CloudCredentials.objects.renew_token()
    return token
