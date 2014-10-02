"""
views.py - `common` app views module.
"""
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    """
    The home page view.
    """
    template_name = 'common/home.html'
