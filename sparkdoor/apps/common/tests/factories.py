"""
factories.py - factory classes for the `common` app's models.
"""
import factory

from sparkdoor.apps.spark.tests.factories import DeviceFactory

from ..models import DoorEvent, DoorPass


class DoorEventFactory(factory.django.DjangoModelFactory):
    """
    Factory class for `models.DoorEvent`.
    """
    class Meta:
        model = DoorEvent

    device = factory.SubFactory(DeviceFactory)
    event = DoorEvent.OPEN_EVENT


class DoorPassFactory(factory.django.DjangoModelFactory):
    """
    Factory class for `models.DoorPass`.
    """
    class Meta:
        model = DoorPass

    token = None
    device = factory.SubFactory(DeviceFactory)
