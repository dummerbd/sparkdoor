"""
factories.py - factory classes for common models.
"""
from django.conf import settings

import factory


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory class for subclasses of `django.contrib.auth.models.User`.
    """
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    first_name = factory.Sequence(lambda n: 'John {0}'.format(n))
    last_name = factory.Sequence(lambda n: 'Doe {0}'.format(n))
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = 'pass1234'
