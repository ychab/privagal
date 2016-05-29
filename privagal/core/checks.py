# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.checks import Critical, Tags, register


@register(Tags.security)
def timeline_password_initial_check(app_configs, **kwargs):
    errors = []

    # Only useful before applying first migration.
    if not settings.PRIVAGAL_TIMELINE_INITIAL_PASSWORD:
        errors.append(
            Critical(
                "PRIVAGAL_TIMELINE_INITIAL_PASSWORD must be set in config.",
                id='privagal_timeline_password_initial',
            )
        )

    return errors
