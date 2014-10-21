"""
tasks.py - `spark` app web worker tasks module.
"""
from django.core.cache import cache

from contextlib import contextmanager

from celery import shared_task
from celery.utils.log import get_task_logger

from .models import CloudCredentials

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 3 # 3 minutex

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
    token = None
    logger.debug('Attempting to acquire lock...')
    with task_lock(key) as locked:
        if locked:
            logger.debug('Lock acquired - getting token...')
            token = CloudCredentials.objects.renew_token()
            logger.debug('Token refreshed.')
        else:
            logger.debug('Lock not acquired.')
            token = CloudCredentials.objects.access_token()
    return token

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param
