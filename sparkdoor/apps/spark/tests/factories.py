"""
factories.py - factory classes for the `spark` app's models.
"""
import factory

from ..models import CloudCredentials


class CloudCredentialsFactory(factory.django.DjangoModelFactory):
    """
    Factory class for `models.CloudCredentials`.
    """
    class Meta:
        model = CloudCredentials

    access_token = None
    expires_at = None
