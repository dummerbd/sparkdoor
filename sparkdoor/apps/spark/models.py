"""
models.py - `spark` app models module.
"""
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone

from .services import SparkCloud
from .settings import SparkSettings


class CloudCredentialsManager(models.Manager):
    """
    Custom model manager for `CloudCredentials`.
    """
    def access_token(self):
        """
        Get the most recent valid `access_token`, if one isn't found
        then None is returned.
        """
        latest = self._latest()
        if latest is None:
            return None
        return latest.access_token

    def refresh_token(self):
        """
        Check if the access token will expire soon, if so then attempt
        to find any existed tokens on the cloud account. If no existing
        tokens are found then a new one will be requested.
        """
        latest = self._latest()
        if latest is None or latest.expires_soon():
            cloud = SparkCloud(SparkSettings().API_URI)
            self._discover_tokens(cloud)
            if self.access_token() is None:
                self._renew_token(cloud)

    def _renew_token(self, cloud):
        """
        Get a new token from the cloud service and record it.
        """
        s = SparkSettings()
        token, expires_at = cloud.renew_token(s.USERNAME, s.PASSWORD)
        CloudCredentials(access_token=token, expires_at=expires_at).save()

    def _discover_tokens(self, cloud):
        """
        Get existing tokens from the cloud service and save the most
        recent.
        """
        s = SparkSettings()
        token, expires_at = cloud.discover_tokens(s.USERNAME, s.PASSWORD)
        if (token is not None and expires_at is not None and
                not self.filter(access_token=token).exists()):
            CloudCredentials(access_token=token, expires_at=expires_at).save()

    def _latest(self):
        """
        Get the latest valid credentials or return None.
        """
        try:
            return self.get_queryset().filter(
                    expires_at__gt=timezone.now()
                ).latest(
                    'expires_at'
                )
        except CloudCredentials.DoesNotExist:
            return None


class CloudCredentials(models.Model):
    """
    Stores credentials to access a Spark cloud service.
    """
    access_token = models.CharField(max_length=250, blank=False, unique=True)
    expires_at = models.DateTimeField()

    def expires_soon(self):
        """
        Determine if these credentials are still within the exipiration
        date.
        """
        window = SparkSettings().RENEW_TOKEN_WINDOW
        return self.expires_at <= (timezone.now() + timedelta(seconds=window))

    objects = CloudCredentialsManager()


class Device(models.Model):
    """
    Stores information about a Spark device.
    """
    device_id = models.CharField(max_length=250, blank=False)
    name = models.CharField(max_length=250, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)

    class Meta:
        unique_together = ('name', 'user')
