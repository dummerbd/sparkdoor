"""
tasks.py - `spark` app web worker tasks module.
"""
from django.core.cache import cache

from contextlib import contextmanager

from celery import shared_task

from .models import CloudCredentials


LOCK_EXPIRE = 60 * 3 # 3 minutes


@contextmanager
def task_lock(key):
    """
    Unique task lock implementation taken from Celery docs here:
    http://celery.readthedocs.org/en/latest/tutorials/task-cookbook.html
    Should probably be replaced with something more robust but will work
    as long as the Django cache backend is setup.

    The context returned is either True or False indicating whether the
    task is unique or not.
    """
    lock_id = '{0}-LOCK'.format(key)
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)
    if acquire_lock():
        yield True
        release_lock()
    else:
        yield False


@shared_task
def refresh_access_token():
    """
    Run this task periodically to check for soon to expire access tokens
    and request a new one when needed.
    """
    key = '{0}.refresh_access_token'.format(__name__)
    with task_lock(key) as locked:
        if locked:
            CloudCredentials.objects.refresh_token()
