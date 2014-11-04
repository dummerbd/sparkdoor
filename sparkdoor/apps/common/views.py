"""
views.py - `common` app views module.
"""
from django.views.generic.base import TemplateView

from braces.views import LoginRequiredMixin


class HomeView(TemplateView):
    """
    The home page view.
    """
    template_name = 'common/home.html'


class DevicesView(LoginRequiredMixin, TemplateView):
    """
    Serves as a user profile page, provides a list of devices for the
    user.
    """
    template_name = 'common/devices.html'

    def get_context_data(self, **kwargs):
        """
        Add a `devices` entry with available devices.
        """
        context = super(DevicesView, self).get_context_data(**kwargs)
        return context
