# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from wagtail.wagtailcore.models import Page

from privagal.gallery.factories import GalleryFactory
from privagal.gallery.models import Gallery
from privagal.timeline.factories import TimelineFactory
from privagal.timeline.models import Timeline


class PageFactoryTestCase(TestCase):
    """
    Test abstract page factory with real models for now (instead of migrating
    conditionnally a dummy page model). In fact, it must be a Wagtail feature,
    not a Privagal feature!
    """

    def tearDown(self):
        Page.objects.type(Timeline).exclude(slug='timeline').delete()

    def test_slug(self):
        page = TimelineFactory()
        self.assertEqual(page.slug, 'timeline_%d' % (int(TimelineFactory._counter.seq) - 1))

    def test_next(self):
        """
        However, this feature may live in factory.DjangoModelFactory itself!
        """
        TimelineFactory()
        # Mimic natural reset (for e.g: in Python shell)
        TimelineFactory.reset_sequence()
        TimelineFactory()
        self.assertNotEqual(TimelineFactory._counter.seq, 1)
