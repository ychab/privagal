# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wagtail.wagtailcore.models import PageViewRestriction

from ..factories import TokenFactory
from ..utils import PrivagalTestCase


class AuthTokenMiddlewareTestCase(PrivagalTestCase):

    def test_no_token_url(self):
        response = self.client.get(self.timeline.url)
        self.assertNotPageLogged(response)

    def test_unknown_token(self):
        response = self.client.get(self.timeline.url, data={'token': 'foo'})
        self.assertNotPageLogged(response)

    def test_token_valid(self):
        token = TokenFactory()
        response = self.client.get(self.timeline.url, data={'token': token.key})
        self.assertPageLogged(response)

    def test_restriction_changed(self):
        token = TokenFactory()
        restriction = PageViewRestriction.objects.get(page=self.timeline)

        self.client.get(self.timeline.url, data={'token': token.key})
        self.assertListEqual(
            self.client.session.get('passed_page_view_restrictions'),
            [restriction.id],
        )
        restriction.delete()

        new_restriction = PageViewRestriction.objects.create(
            page=self.timeline, password='foo')
        self.client.get(self.timeline.url, data={'token': token.key})
        self.assertListEqual(
            self.client.session.get('passed_page_view_restrictions'),
            [new_restriction.id],
        )
