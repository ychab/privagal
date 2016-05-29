# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class TokenModelAdminFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            'foo', is_staff=True, is_superuser=True)

    def test_default_token_value(self):
        url = reverse('core_token_modeladmin_create')
        self.client.force_login(self.user)
        response = self.client.get(url)
        form = response.context_data['form']
        self.assertTrue(form.initial['key'])
