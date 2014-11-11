"""
views.py - `common` app views module.
"""
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin

from sparkdoor.apps.spark.forms import RegisterDeviceForm
from sparkdoor.apps.spark.models import Device


class HomeView(TemplateView):
    """
    The home page view.
    """
    template_name = 'common/home.html'


class DevicesView(LoginRequiredMixin, CreateView):
    """
    Serves as a user profile page, provides a list of devices for the
    user.
    """
    template_name = 'common/devices.html'
    form_class = RegisterDeviceForm

    def get_context_data(self, **kwargs):
        """
        Add a `devices` entry with available devices.
        """
        context = super(DevicesView, self).get_context_data(**kwargs)
        context['devices'] = Device.objects.for_user(self.request.user).order_by('name')
        return context
