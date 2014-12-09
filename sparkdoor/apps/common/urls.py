"""
urls.py - `common` app url routes module.
"""
from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^api/id-card-open$',
        views.IDCardOpenView.as_view(),
        name='id-card-open'
    ),

    url(r'^profile$',
        views.ProfileView.as_view(),
        name='profile'
    ),

    url(r'^$',
        views.HomeView.as_view(),
        name='home'
    )
)
