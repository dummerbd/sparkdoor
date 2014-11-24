"""
factories.py - factory classes for the `spark` app's models.
"""
from datetime import timedelta

from django.utils import timezone

import factory

from sparkdoor.libs.factories import UserFactory

from ..models import CloudCredentials, Device


class CloudCredentialsFactory(factory.django.DjangoModelFactory):
    """
    Factory class for `models.CloudCredentials`.
    """
    class Meta:
        model = CloudCredentials

    access_token = None
    expires_at = timezone.now() + timedelta(days=90)


class DeviceFactory(factory.django.DjangoModelFactory):
    """
    Factory class for `models.Device`.
    """
    class Meta:
        model = Device

    device_id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: 'device-{0}'.format(n))
    user = factory.SubFactory(UserFactory)
    app_name = factory.Sequence(lambda n: 'app-{0}'.format(n))
