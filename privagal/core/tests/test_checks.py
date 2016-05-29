# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.checks import Critical, run_checks
from django.test import SimpleTestCase, override_settings


class TimelinePasswordInitialCheck(SimpleTestCase):

    @override_settings(PRIVAGAL_TIMELINE_INITIAL_PASSWORD='')
    def test_missing_setting(self):
        msgs = run_checks()
        errors = self.filter_msgs(msgs)
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], Critical)

    @override_settings(PRIVAGAL_TIMELINE_INITIAL_PASSWORD='foo')
    def test_check_pass(self):
        msgs = run_checks()
        errors = self.filter_msgs(msgs)
        self.assertFalse(errors)

    def filter_msgs(self, msgs):
        return [msg for msg in msgs if msg.id == 'privagal_timeline_password_initial']
