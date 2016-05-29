# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.views.i18n import javascript_catalog

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls

from privagal.core import urls as privagalcore_urls

urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),

    url(r'^jsi18n/$', javascript_catalog, name='javascript-catalog'),

    url(r'^gallery/', include('privagal.gallery.urls', namespace='galleries')),
    url(r'^{}'.format(settings.MEDIA_URL[1:]), include(privagalcore_urls)),

    url(r'', include(wagtail_urls)),
]
