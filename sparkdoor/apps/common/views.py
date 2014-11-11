"""
views.py - `common` app views module.
"""
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin, FormMessagesMixin

from sparkdoor.apps.spark.forms import RegisterDeviceForm
from sparkdoor.apps.spark.models import Device


class HomeView(TemplateView):
    """
    The home page view.
    """
    template_name = 'common/home.html'


class DevicesView(LoginRequiredMixin, FormMessagesMixin, CreateView):
    """
    Serves as a user profile page, provides a list of devices for the
    user.
    """
    template_name = 'common/devices.html'
    form_class = RegisterDeviceForm
    success_url = reverse_lazy('common:devices')
    form_invalid_message = 'Could not register device'

    def get_form_valid_message(self):
        return 'Added {0} device'.format(self.object.name)

    def get_context_data(self, **kwargs):
        """
        Add a `devices` entry with available devices.
        """
        context = super(DevicesView, self).get_context_data(**kwargs)
        context['devices'] = Device.objects.for_user(self.request.user).order_by('name')
        return context

    def post(self, request, *args, **kwargs):
        """
        Add the user of this request.
        """
        request.POST = request.POST.copy()
        request.POST['user'] = self.request.user.id
        return super(DevicesView, self).post(request, *args, **kwargs)
