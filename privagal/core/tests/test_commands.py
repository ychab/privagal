# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import get_image_model

from privagal.gallery.factories import GalleryFactory
from privagal.gallery.models import Gallery

from ..management.commands.genfactories import IMAGES

Image = get_image_model()


class GenerateFactoriesTestCase(TestCase):

    def test_generate(self):
        Page.objects.type(Gallery).delete()

        out = StringIO()
        call_command('genfactories', interactive=False, stdout=out)
        self.assertEqual(Page.objects.type(Gallery).count(), 5)
        self.assertIn(
            'Galleries have been generated successfully.\n',
            out.getvalue(),
        )

    def test_purge(self):
        for i in range(0, 3):
            GalleryFactory()

        out = StringIO()
        call_command(
            'genfactories', interactive=False, stdout=out, purge=True, limit=1)
        self.assertEqual(Page.objects.type(Gallery).count(), 1)
        self.assertEqual(Image.objects.all().count(), len(IMAGES))

    def test_limit(self):
        Page.objects.type(Gallery).delete()

        out = StringIO()
        call_command(
            'genfactories', interactive=False, stdout=out, limit=10)
        self.assertEqual(Page.objects.type(Gallery).count(), 10)
