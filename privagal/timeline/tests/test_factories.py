# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from wagtail.wagtailcore.models import Page

from privagal.gallery.factories import GalleryFactory

from ..factories import TimelineFactory
from ..models import Timeline


class TimelineFactoryTestCase(TestCase):

    def tearDown(self):
        Page.objects.type(Timeline).exclude(slug='timeline').delete()

    def test_create_strategy(self):
        timeline = TimelineFactory()
        self.assertTrue(timeline.pk)
        self.assertEqual(timeline.path, '00010002')
        self.assertEqual(timeline.depth, 2)

    def test_add_sibling(self):
        TimelineFactory()
        timeline = TimelineFactory()
        self.assertEqual(timeline.path, '00010003')

    def test_build_strategy(self):
        timeline = TimelineFactory(create=False)
        self.assertFalse(timeline.pk)

    def test_add_galleries(self):
        gallery_1 = GalleryFactory()
        gallery_2 = GalleryFactory()
        timeline = TimelineFactory(galleries=[gallery_1, gallery_2])
        self.assertListEqual(
            [gallery_1.pk, gallery_2.pk],
            [g.pk for g in timeline.get_children().order_by('pk')],
        )
