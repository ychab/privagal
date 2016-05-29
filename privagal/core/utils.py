# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.test import Client, TestCase

from wagtail.wagtailcore.models import Page


def check_view_restrictions(request, page):
    """
    Mimic default Wagtail core behaviour but throw a 403 exception instead of
    a redirect.

    See wagtail.wagtailcore.wagtail_hooks.check_view_restrictions
    """
    restrictions = page.get_view_restrictions()
    if restrictions:
        passed_restrictions = request.session.get('passed_page_view_restrictions', [])

        for restriction in restrictions:
            if restriction.id not in passed_restrictions:
                raise PermissionDenied


class PrivagalClient(Client):

    session_cookie = settings.SESSION_COOKIE_NAME

    def page_login(self):
        page = Page.objects.get(slug='timeline')
        session = self.session
        session['passed_page_view_restrictions'] = [
            restriction.id for restriction in page.get_view_restrictions()]
        session.save()

    def page_logout(self):
        session = self.session
        session['passed_page_view_restrictions'] = []
        session.save()


class PrivagalTestCase(TestCase):
    client_class = PrivagalClient
    login_template_name = None

    @classmethod
    def setUpClass(cls):
        super(PrivagalTestCase, cls).setUpClass()
        if settings.PRIVAGAL_AUTH_TOKEN_REQUIRED:
            cls.login_template_name = 'token_required.html'
        else:
            cls.login_template_name = 'password_required.html'

    @classmethod
    def setUpTestData(cls):
        cls.timeline = Page.objects.get(slug='timeline').specific

    def assertPageLogged(self, response):
        self.assertTemplateNotUsed(
            response, self.login_template_name, msg_prefix='Not page logged in')

    def assertNotPageLogged(self, response):
        self.assertTemplateUsed(
            response, self.login_template_name, msg_prefix='Page logged in')
