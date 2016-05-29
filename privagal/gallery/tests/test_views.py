# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import tempfile
import zipfile

from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse

from privagal.core.utils import PrivagalTestCase

from ..factories import GalleryFactory


class GalleryDetailPageAccessViewTestCase(PrivagalTestCase):

    @classmethod
    def setUpTestData(cls):
        super(GalleryDetailPageAccessViewTestCase, cls).setUpTestData()
        cls.gallery = GalleryFactory()
        cls.timeline.add_child(instance=cls.gallery)

    def test_no_password_denied(self):
        response = self.client.get(self.gallery.url, follow=False)
        self.assertNotPageLogged(response)

    def test_password_allowed(self):
        self.client.page_login()
        response = self.client.get(self.gallery.url, follow=True)
        self.assertPageLogged(response)


class GalleryDownloadViewTestCase(PrivagalTestCase):

    @classmethod
    def setUpTestData(cls):
        super(GalleryDownloadViewTestCase, cls).setUpTestData()

        cls.gallery = GalleryFactory()
        cls.timeline.add_child(instance=cls.gallery)
        cls.url = reverse('galleries:download', kwargs={'pk': cls.gallery.pk})

    def test_access_no_password_denied(self):
        response = self.client.get(self.url, follow=False)
        self.assertEqual(response.status_code, 403)

    def test_access_authentificated_allow(self):
        self.client.page_login()
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_archive_dir_create(self):
        media_root = tempfile.mkdtemp()

        self.client.page_login()
        with self.settings(MEDIA_ROOT=media_root):
            gallery = GalleryFactory()
            self.timeline.add_child(instance=gallery)
            url = reverse('galleries:download', kwargs={'pk': gallery.pk})

            self.client.get(url)

        self.assertTrue(os.path.exists(os.path.join(media_root, 'archives')))

    def test_archive_dir_exists(self):
        media_root = tempfile.mkdtemp()

        self.client.page_login()
        with self.settings(MEDIA_ROOT=media_root):
            gallery = GalleryFactory()
            self.timeline.add_child(instance=gallery)
            url = reverse('galleries:download', kwargs={'pk': gallery.pk})

            self.client.get(url)
            response = self.client.get(url)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(os.path.exists(os.path.join(media_root, 'archives')))

    def test_download_zip(self):
        self.client.page_login()
        response = self.client.get(self.url, follow=True)

        self.assertEqual(response['content-type'], 'application/zip')
        self.assertIn('attachment; filename=', response['content-disposition'])
        self.assertIn(
            '{gallery.date}-{gallery.pk}.zip'.format(gallery=self.gallery),
            response['content-disposition'],
        )
        self.assertTrue(response.streaming)

        images = [i.image.file for i in self.gallery.images.prefetch_related('image').all()]

        zf = zipfile.ZipFile(ContentFile(response.getvalue()), 'r')
        zipinfo = zf.infolist()
        self.assertEqual(len(zipinfo), 3)
        self.assertEqual(zipinfo[0].filename, os.path.basename(images[0].name))
        self.assertEqual(zipinfo[1].filename, os.path.basename(images[1].name))
        self.assertEqual(zipinfo[2].filename, os.path.basename(images[2].name))
