# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import binascii
import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class TokenManager(models.Manager):

    def singleton(self):
        if not hasattr(self, '_singleton'):
            try:
                self._singleton = self.latest()
            except self.model.DoesNotExist:
                self._singleton = None
        return self._singleton

    def reset_singleton(self):
        if hasattr(self, '_singleton'):
            del self._singleton


@python_2_unicode_compatible
class Token(models.Model):
    """
    Heavily copied from rest_framework.authtoken.models.Token
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    objects = TokenManager()

    class Meta:
        db_table = 'privagal_token'
        get_latest_by = "created"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = Token.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return self.key

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
