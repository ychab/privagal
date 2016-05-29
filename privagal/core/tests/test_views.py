# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

from wagtail.wagtailimages.views.serve import generate_signature

from privagal.gallery.factories import GalleryFactory, ImageFactory
from privagal.timeline.models import Timeline

from ..utils import PrivagalTestCase

try:
    from unittest import mock  # pragma: no cover
except ImportError:
    import mock


class SendFilePrivateViewTestCase(PrivagalTestCase):

    @classmethod
    def setUpTestData(cls):
        super(SendFilePrivateViewTestCase, cls).setUpTestData()

        cls.image = ImageFactory()
        cls.filter_spec = 'max-200x150'
        cls.signature = generate_signature(cls.image.id, cls.filter_spec)

        cls.url = reverse('wagtailimages_serve', args=(
            cls.signature, cls.image.id, cls.filter_spec))

    def test_access_anonymous_denied(self):
        response = self.client.get(self.url, follow=False)
        self.assertEqual(response.status_code, 403)

    def test_invalid_signature(self):
        url = reverse('wagtailimages_serve', args=(
            'foo', self.image.id, self.filter_spec))

        self.client.page_login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_unknown_image(self):
        image_id = 9999999999
        signature = generate_signature(image_id, self.filter_spec)
        url = reverse('wagtailimages_serve', args=(
            signature, image_id, self.filter_spec))
        self.client.page_login()

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unknown_spec(self):
        signature = generate_signature(self.image.id, 'foo')
        url = reverse('wagtailimages_serve', args=(
            signature, self.image.id, 'foo'))

        self.client.page_login()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_sendfile(self):
        self.client.page_login()
        response = self.client.get(self.url)
        self.assertTrue(response.streaming)
        self.assertEqual(response['content-type'], 'image/jpeg')


@override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'media'))
class BackOfficeSendFileViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            'foo', password='foo', is_staff=True)
        cls.url = reverse(
            'backoffice_serve',
            kwargs={'filepath': os.path.join('tests', 'django.png')},
        )
        cls.target_dir = os.path.join(settings.MEDIA_ROOT, 'tests')
        try:
            os.makedirs(cls.target_dir)
        except os.error:
            pass

        src = os.path.join(settings.PROJECT_DIR, 'core', 'tests', 'assets', 'django.png')
        shutil.copy(src, cls.target_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.target_dir)
        super(BackOfficeSendFileViewTestCase, cls).tearDownClass()

    def test_is_not_staff(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_serve(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTrue(response.streaming)
        self.assertEqual(response['content-type'], 'image/png')


class TimelineViewTestCase(PrivagalTestCase):

    @mock.patch.object(Timeline, 'paginate_by', new_callable=mock.PropertyMock)
    def test_pager_link(self, mock_page_size):
        limit = 3
        mock_page_size.return_value = limit

        for i in range(0, limit + 1):
            gallery = GalleryFactory(title="foo")
            self.timeline.add_child(instance=gallery)

        self.client.page_login()
        response = self.client.get(self.timeline.url, data={'query': 'foo'})

        self.assertContains(
            response,
            'href="?page=2&query=foo"'.format(timeline=self.timeline.url),
        )
