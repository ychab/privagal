# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from ..factories import TokenFactory
from ..models import Token


class TokenManagerTestCase(TestCase):

    def setUp(self):
        Token.objects.all().delete()
        Token.objects.reset_singleton()

    def test_no_token(self):
        self.assertIsNone(Token.objects.singleton())

    def test_singleton_cache_with_no_token(self):
        """
        Don't try request, even if there is no token.
        """
        self.assertNumQueries(1, func=Token.objects.singleton)
        self.assertNumQueries(0, func=Token.objects.singleton)

    def test_singleton_reset(self):
        """
        Redo request if asked.
        """
        self.assertNumQueries(1, func=Token.objects.singleton)
        Token.objects.reset_singleton()
        self.assertNumQueries(1, func=Token.objects.singleton)

    def test_singleton_reset_twice(self):
        """
        You can't delete an attribute which doesn't exists!
        """
        Token.objects.reset_singleton()
        Token.objects.reset_singleton()


class TokenTestCase(TestCase):

    def test_auto_key(self):
        token = TokenFactory()
        self.assertTrue(token.key)

    def test_no_auto_key(self):
        token = TokenFactory(key='hackable_password')
        self.assertEqual(token.key, 'hackable_password')
