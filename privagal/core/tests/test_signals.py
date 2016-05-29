# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from ..factories import TokenFactory
from ..models import Token


class TokenResetSingletonTestCase(TestCase):

    def test_signal_insert_token(self):
        token = TokenFactory()
        singleton = Token.objects.singleton()
        self.assertEqual(token, singleton)

        token = TokenFactory()
        singleton = Token.objects.singleton()
        self.assertEqual(token, singleton)

    def test_signal_delete_last_token(self):
        token1 = TokenFactory()
        token2 = TokenFactory()
        singleton = Token.objects.singleton()
        self.assertEqual(token2, singleton)

        token2.delete()
        singleton = Token.objects.singleton()
        self.assertEqual(token1, singleton)
