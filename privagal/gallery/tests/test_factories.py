# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from privagal.core.utils import PrivagalTestCase

from ...gallery.factories import GalleryFactory, ImageFactory


class GalleryFactoryTestCase(PrivagalTestCase):

    def test_images_given(self):
        image = ImageFactory()
        gallery = GalleryFactory(images__images=[image])
        self.timeline.add_child(instance=gallery)
        self.assertEqual(gallery.images.first().image, image)

    def test_images_default(self):
        gallery = GalleryFactory()
        self.assertEqual(gallery.images.count(), 3)
