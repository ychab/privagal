# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import override_settings

from privagal.gallery.factories import GalleryFactory

from ..utils import PrivagalTestCase


@override_settings(PRIVAGAL_AUTH_TOKEN_REQUIRED=False)
class AuthTokenNotRequiredTestCase(PrivagalTestCase):

    @classmethod
    def setUpTestData(cls):
        super(AuthTokenNotRequiredTestCase, cls).setUpTestData()
        cls.gallery = GalleryFactory()
        cls.timeline.add_child(instance=cls.gallery)

    def test_password_required_timeline(self):
        response = self.client.get(self.timeline.url)
        self.assertTemplateUsed(response, 'password_required.html')

    def test_password_required_gallery(self):
        response = self.client.get(self.gallery.url)
        self.assertTemplateUsed(response, 'password_required.html')


@override_settings(PRIVAGAL_AUTH_TOKEN_REQUIRED=True)
class AuthTokenRequiredTestCase(PrivagalTestCase):

    @classmethod
    def setUpTestData(cls):
        super(AuthTokenRequiredTestCase, cls).setUpTestData()
        cls.user_staff = get_user_model().objects.create_user(
            'foo', is_staff=True)
        cls.gallery = GalleryFactory()
        cls.timeline.add_child(instance=cls.gallery)

    def test_is_staff(self):
        self.client.force_login(self.user_staff)
        response = self.client.get(self.timeline.url)
        self.assertTemplateUsed(response, 'password_required.html')

    def test_token_required_timeline(self):
        response = self.client.get(self.timeline.url)
        self.assertTemplateUsed(response, 'token_required.html')

    def test_token_required_gallery(self):
        response = self.client.get(self.gallery.url)
        self.assertTemplateUsed(response, 'token_required.html')
