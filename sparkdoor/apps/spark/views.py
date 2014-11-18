"""
views.py - `spark` app views module.
"""
from django.views.generic.edit import CreateView

from braces.views import LoginRequiredMixin, FormMessagesMixin

from .forms import RegisterDeviceForm
from .models import Device


class DeviceAppBase:
    """
    Base class for Spark device apps. This class is responsible for
    rendering a device in the `UserDevicesViewBase` subclasses.
    """
    def __init__(self, device):
        """
        Constructor.
        """
        self.device = device

    def status(self, name):
        """
        Handle a status read.
        """
        raise NotImplementedError

    def command(self, cmd):
        """
        Handle a command action.
        """
        raise NotImplementedError

    def render(self):
        """
        Render this device as HTML.
        """
        raise NotImplementedError


class UserDevicesViewBase(LoginRequiredMixin, FormMessagesMixin, CreateView):
    """
    View base class for listing a user's devices by delegating rendering
    to a `DeviceAppBase` subclass for that device's `app_name`. A new
    device registration form is also provided.

    Subclasses must define the following attributes:
        `template_name` - The template to render.
        `success_url` - Should be the url for this view. This is where
            the user is redirected to after they submit the registration
            form.
    """
    form_class = RegisterDeviceForm
    form_invalid_message = 'Could not register device'

    def get_form_valid_message(self):
        return 'Added {0} device'.format(self.object.name)

    def get_context_data(self, **kwargs):
        """
        Add a `devices` entry with available devices.
        """
        context = super(UserDevicesViewBase, self).get_context_data(**kwargs)
        context['devices'] = Device.objects.for_user(self.request.user).order_by('name')
        return context

    def post(self, request, *args, **kwargs):
        """
        Add the user of this request.
        """
        request.POST = request.POST.copy()
        request.POST['user'] = self.request.user.id
        return super(UserDevicesViewBase, self).post(request, *args, **kwargs)
