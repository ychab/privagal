# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import BackOfficeSendFileView, SendFilePrivateView

urlpatterns = [
    url(
        r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$',
        SendFilePrivateView.as_view(),
        name='wagtailimages_serve'
    ),
    url(
        r'(?P<filepath>.*)$',
        BackOfficeSendFileView.as_view(),
        name='backoffice_serve'
    ),
]
