# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.test import TestCase

from privagal.gallery.factories import ImageFactory

from ..templatetags.privagalcore_tags import image_url


class ImageUrlTestCase(TestCase):

    def test_image_url(self):
        image = ImageFactory()
        filter_spec = 'max200-150'
        url = image_url(image, filter_spec)

        self.assertRegexpMatches(
            url,
            '^{media}images/(.)*/{filter_spec}/{filename}$'.format(
                media=settings.MEDIA_URL,
                filter_spec=filter_spec,
                filename=image.filename,
            )
        )
