# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import get_image_model

from privagal.core.utils import PrivagalTestCase

from ..factories import GalleryFactory, ImageFactory, ImageGalleryFactory
from ..models import ImageGallery

Image = get_image_model()

try:
    from unittest import mock  # pragma: no cover
except ImportError:
    import mock


class ImageGalleryModelRelationshipTestCase(PrivagalTestCase):

    def setUp(self):
        self.image = ImageFactory()
        self.gallery = GalleryFactory(images__images=[self.image])
        self.timeline.refresh_from_db()
        self.timeline.add_child(instance=self.gallery)
        self.image_gallery = self.gallery.images.first()

    def test_delete_gallery_cascade_image_gallery(self):
        self.gallery.delete()
        with self.assertRaises(ImageGallery.DoesNotExist):
            self.image_gallery.refresh_from_db()

    def test_delete_gallery_cascade_image(self):
        image_2 = ImageFactory()
        image_gallery_2 = ImageGalleryFactory(page=self.gallery, image=image_2)
        self.gallery.images.add(image_gallery_2)

        self.gallery.delete()
        with self.assertRaises(Image.DoesNotExist):
            self.image.refresh_from_db()
        with self.assertRaises(Image.DoesNotExist):
            image_2.refresh_from_db()

    @mock.patch.object(Image, 'delete', side_effect=Exception('Boom'))
    def test_delete_gallery_fail(self, mock_delete):
        with self.assertRaises(Exception):
            self.gallery.delete()

        self.image.refresh_from_db()
        self.gallery.refresh_from_db()

    def test_delete_image_gallery_not_gallery(self):
        self.image_gallery.delete()
        self.gallery.refresh_from_db()
        self.assertFalse(self.gallery.images.all())

    def test_delete_image_gallery_cascade_image(self):
        self.image_gallery.delete()
        with self.assertRaises(Image.DoesNotExist):
            self.image.refresh_from_db()

    @mock.patch.object(ImageGallery, 'delete', side_effect=Exception('Boom'))
    def test_delete_image_gallery_fail(self, mock_delete):
        image_gallery_id = self.image_gallery.id
        with self.assertRaises(Exception):
            self.image_gallery.delete()
        self.image.refresh_from_db()
        self.assertTrue(ImageGallery.objects.get(id=image_gallery_id))

    def test_delete_image_not_gallery(self):
        self.image.delete()
        self.gallery.refresh_from_db()
        self.assertFalse(self.gallery.images.all())

    def test_delete_image_cascade_image_gallery(self):
        self.image.delete()
        with self.assertRaises(ImageGallery.DoesNotExist):
            self.image_gallery.refresh_from_db()


class ImageGalleryQuerysetRelationshipTestCase(PrivagalTestCase):

    def setUp(self):
        self.image = ImageFactory()
        self.gallery = GalleryFactory(images__images=[self.image])
        self.timeline.refresh_from_db()
        self.timeline.add_child(instance=self.gallery)
        self.image_gallery = self.gallery.images.first()

    def test_delete_gallery_cascade_image_gallery(self):
        Page.objects.get(pk=self.gallery.pk).delete()
        with self.assertRaises(ImageGallery.DoesNotExist):
            self.image_gallery.refresh_from_db()

    @unittest.expectedFailure
    def test_delete_gallery_cascade_image(self):
        """
        Unfortunetly, we cannot do this easily (except overriding queryset
        manager?). So we must be careful with this...
        """
        Page.objects.get(pk=self.gallery.pk).delete()
        with self.assertRaises(Image.DoesNotExist):
            self.image.refresh_from_db()

    def test_delete_image_cascade_image_gallery(self):
        Image.objects.get(pk=self.image.pk).delete()
        with self.assertRaises(ImageGallery.DoesNotExist):
            self.image_gallery.refresh_from_db()
