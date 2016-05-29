# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from ..models import Token


@receiver(post_save, sender=Token)
def token_save_reset_singleton(sender, instance=None, created=False, **kwargs):
    Token.objects.reset_singleton()


@receiver(post_delete, sender=Token)
def token_delete_reset_singleton(sender, instance=None, created=False, **kwargs):
    Token.objects.reset_singleton()
