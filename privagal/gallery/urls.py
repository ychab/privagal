# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import GalleryDownloadView

urlpatterns = [
    url(
        r'^(?P<pk>\d+)/download/$',
        GalleryDownloadView.as_view(),
        name='download',
    ),
]
