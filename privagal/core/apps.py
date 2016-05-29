# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class PrivagalConfig(AppConfig):
    name = 'privagal.core'
    verbose_name = "Privagal"

    def ready(self):
        import privagal.core.checks  # noqa
        import privagal.core.signals.handlers  # noqa
