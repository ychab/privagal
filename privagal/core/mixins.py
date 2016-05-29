# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.template.response import TemplateResponse

from wagtail.wagtailcore.models import Page

from .utils import check_view_restrictions


class PageLoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        page = Page.objects.get(slug='timeline')
        check_view_restrictions(request, page)
        return super(PageLoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class AuthTokenPageMixin(object):

    def serve_password_required_response(self, request, form, action_url):
        if not request.user.is_staff and settings.PRIVAGAL_AUTH_TOKEN_REQUIRED:
            return TemplateResponse(request, 'token_required.html')

        return super(AuthTokenPageMixin, self).serve_password_required_response(
            request, form, action_url)
