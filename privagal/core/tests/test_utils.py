# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.test import RequestFactory

from wagtail.wagtailcore.models import PageViewRestriction

from privagal.timeline.factories import TimelineFactory

from ..utils import PrivagalTestCase, check_view_restrictions


class PageAuthTestCase(PrivagalTestCase):

    def test_password_required(self):
        response = self.client.get(self.timeline.url)
        self.assertNotPageLogged(response)

    def test_page_login(self):
        self.client.page_login()
        response = self.client.get(self.timeline.url)
        self.assertPageLogged(response)

    def test_page_logout(self):
        self.client.page_login()
        response = self.client.get(self.timeline.url)
        self.assertPageLogged(response)

        self.client.page_logout()
        response = self.client.get(self.timeline.url)
        self.assertNotPageLogged(response)


class PageCheckRestrictionTestCase(PrivagalTestCase):

    def test_no_restriction(self):
        self.client.page_logout()
        check_view_restrictions(RequestFactory(), TimelineFactory())

    def test_no_passed_restriction(self):
        page = TimelineFactory()
        PageViewRestriction.objects.create(page=page, password='foo')

        session = self.client.session
        session['passed_page_view_restrictions'] = []
        session.save()
        request = RequestFactory()
        request.session = session

        with self.assertRaises(PermissionDenied):
            check_view_restrictions(request, page)

    def test_not_all_restrictions(self):
        page = TimelineFactory()
        restriction = PageViewRestriction.objects.create(page=page, password='foo')
        PageViewRestriction.objects.create(page=page, password='bar')

        session = self.client.session
        session['passed_page_view_restrictions'] = [restriction.id]
        session.save()
        request = RequestFactory()
        request.session = session

        with self.assertRaises(PermissionDenied):
            check_view_restrictions(request, page)

    def test_passed_restriction(self):
        page = TimelineFactory()
        restriction = PageViewRestriction.objects.create(page=page, password='foo')

        session = self.client.session
        session['passed_page_view_restrictions'] = [restriction.id]
        session.save()
        request = RequestFactory()
        request.session = session

        check_view_restrictions(request, page)
