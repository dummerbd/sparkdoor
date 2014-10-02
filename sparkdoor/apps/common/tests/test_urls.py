"""
test_urls.py - test cases for the `common` app's urls module.
"""
from django.test import SimpleTestCase
from django.core.urlresolvers import reverse


class CommonUrlsTestCase(SimpleTestCase):
    """
    Test case for all url routes in the `common` app.
    """
    urls = 'sparkdoor.apps.common.urls'

    def test_home_can_be_reversed(self):
        """
        Test that the `home` route is valid.
        """
        self.assertTrue(reverse('home'))
