"""
urls.py - top-level url routes module.
"""
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^api/',
        include('sparkdoor.apps.spark.urls')
    ),

    url(r'^admin/',
        include(admin.site.urls)
    ),

    url(r'^accounts/',
        include('allauth.urls')
    ),

    # this needs to be last:
    url(r'^',
        include('sparkdoor.apps.common.urls', namespace='common')
    )
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug_toolbar__/',
            include(debug_toolbar.urls)
        )
    )
