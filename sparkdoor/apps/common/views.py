"""
views.py - `common` app views module.
"""
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView

from sparkdoor.apps.spark.views import UserDevicesViewBase


class HomeView(TemplateView):
    """
    The home page view.
    """
    template_name = 'common/home.html'


class ProfileView(UserDevicesViewBase):
    """
    The user profile view, which provides a list of the user's devices
    and a device registration form.
    """
    template_name = 'common/devices.html'
    success_url = reverse_lazy('common:profile')

class QrcodeView(TemplateView):
    template_name = 'common/qrcode.html'