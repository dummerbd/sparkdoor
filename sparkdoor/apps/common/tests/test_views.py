"""
test_views.py - test cases for the `common` app's view module.
"""
from django.test import SimpleTestCase

from sparkdoor.libs.testmixins import ViewsTestMixin

from .. import views


class HomeViewTestCase(ViewsTestMixin, SimpleTestCase):
    """
    Test case for `views.HomeView`.
    """
    view_class = views.HomeView

    def test_correct_template(self):
        """
        Test that the correct template is used.
        """
        self.assertCorrectTemplateUsed('common/home.html')
