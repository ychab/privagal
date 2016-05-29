# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.views.generic import View

from wagtail.contrib.modeladmin.views import CreateView
from wagtail.wagtailimages.views.serve import SendFileView

from sendfile import sendfile

from .mixins import PageLoginRequiredMixin
from .models import Token


class SendFilePrivateView(PageLoginRequiredMixin, SendFileView):
    pass


class BackOfficeSendFileView(View):

    def dispatch(self, request, filepath, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        # No need to check file to serve: we blindly rely on backend. For
        # example, you need to properly configure nginx to **only** serve
        # private file from that directory. Same goes for Apache.
        path = os.path.join(settings.MEDIA_ROOT, filepath)
        return sendfile(request, path)


class TokenCreateView(CreateView):

    def get_initial(self):
        initial = super(TokenCreateView, self).get_initial()
        initial['key'] = Token.generate_key()
        return initial
