"""
factories.py - factory classes for the `spark` app's models.
"""
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
    expires_at = None


class DeviceFactory(factory.django.DjangoModelFactory):
    """
    Factory class for `models.Device`.
    """
    class Meta:
        model = Device

    device_id = None
    name = factory.Sequence(lambda n: 'device-{0}'.format(n))
    user = factory.SubFactory(UserFactory)
