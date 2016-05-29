# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from privagal.gallery.factories import GalleryFactory

from ..factories import TokenFactory
from ..models import Token
from ..utils import PrivagalTestCase


class TokenLinkMoreButtonTestCase(PrivagalTestCase):

    @classmethod
    def setUpTestData(cls):
        super(TokenLinkMoreButtonTestCase, cls).setUpTestData()
        cls.user = get_user_model().objects.create_user(
            'foo', is_staff=True, is_superuser=True)

    def tearDown(self):
        Token.objects.all().delete()

    def test_url_share(self):
        token = TokenFactory()
        gallery = GalleryFactory()
        self.timeline.add_child(instance=gallery)

        url = reverse('wagtailadmin_explore', args=(self.timeline.id,))
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertContains(response, 'href="{url}?token={key}"'.format(
            url=gallery.full_url,
            key=token.key,
        ))

    def test_no_token(self):
        url = reverse('wagtailadmin_explore_root')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertNotContains(response, '?token=')

    def test_no_root_url_share(self):
        """
        We should only have the timeline token link, no one for the root page.
        """
        TokenFactory()
        url = reverse('wagtailadmin_explore_root')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertContains(response, '?token=', count=1)
