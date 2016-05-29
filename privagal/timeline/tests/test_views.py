# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from wagtail.wagtailcore.models import Page

from privagal.core.utils import PrivagalTestCase
from privagal.gallery.factories import GalleryFactory
from privagal.gallery.models import Gallery

from ..models import Timeline

try:
    from unittest import mock  # pragma: no cover
except ImportError:
    import mock


class TimelineSearchViewTestCase(PrivagalTestCase):

    @classmethod
    def setUpTestData(cls):
        super(TimelineSearchViewTestCase, cls).setUpTestData()

        cls.galleries = []
        for title in ['foo', 'bar']:
            gallery = GalleryFactory(title=title)
            cls.timeline.add_child(instance=gallery)
            cls.galleries.append(gallery)

    def test_search_result(self):
        self.client.page_login()
        response = self.client.get(self.timeline.url, data={'query': 'foo'})
        self.assertListEqual(
            [obj.pk for obj in response.context['object_list']],
            [self.galleries[0].pk],
        )

    def test_search_no_result(self):
        self.client.page_login()
        response = self.client.get(self.timeline.url, data={'query': 'baz'})
        self.assertFalse(response.context['object_list'])


class TimelinePaginationViewTestCase(PrivagalTestCase):

    @classmethod
    def setUpTestData(cls):
        super(TimelinePaginationViewTestCase, cls).setUpTestData()
        cls.limit = 3
        cls.pages = 2
        for i in range(0, cls.limit * cls.pages):
            cls.timeline.add_child(instance=GalleryFactory())

    def setUp(self):
        self.patch = mock.patch.object(
            Timeline, 'paginate_by', new_callable=mock.PropertyMock)
        limit = self.patch.start()
        limit.return_value = self.limit

    def tearDown(self):
        self.patch.stop()

    def test_pagination(self):
        self.client.page_login()
        response = self.client.get(self.timeline.url)
        self.assertEqual(response.context['object_list'].count(), self.limit)

    def test_page_not_integer(self):
        self.client.page_login()
        response = self.client.get(self.timeline.url, data={'page': 'foo'})
        self.assertEqual(response.context['page_obj'].number, 1)

    def test_page_out_range(self):
        self.client.page_login()
        response = self.client.get(self.timeline.url, data={'page': self.pages + 1})
        self.assertEqual(response.context['page_obj'].number, 1)


class TimelineViewTestCase(PrivagalTestCase):

    def setUp(self):
        Page.objects.type(Gallery).delete()
        self.timeline.refresh_from_db()

    def test_unpublished(self):
        self.timeline.add_child(instance=GalleryFactory(live=True))
        self.timeline.add_child(instance=GalleryFactory(live=False))

        self.client.page_login()
        response = self.client.get(self.timeline.url)
        self.assertEqual(response.context['object_list'].count(), 1)

    def test_order_by_date(self):
        gallery_0 = GalleryFactory(date=datetime.date(2016, 4, 28))
        self.timeline.add_child(instance=gallery_0)

        gallery_1 = GalleryFactory(date=datetime.date(2016, 4, 29))
        self.timeline.add_child(instance=gallery_1)

        self.client.page_login()
        response = self.client.get(self.timeline.url)

        galleries = list(response.context['object_list'])
        self.assertEqual(galleries[0], gallery_1)
        self.assertEqual(galleries[1], gallery_0)


class TimelineAccessViewTestCase(PrivagalTestCase):

    def test_no_password_denied(self):
        response = self.client.get(self.timeline.url)
        self.assertNotPageLogged(response)

    def test_password_allowed(self):
        self.client.page_login()
        response = self.client.get(self.timeline.url)
        self.assertPageLogged(response)
