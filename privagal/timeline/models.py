# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Prefetch

from wagtail.utils.pagination import paginate
from wagtail.wagtailcore.models import Page

from privagal.core.mixins import AuthTokenPageMixin
from privagal.gallery.models import Gallery, ImageGallery


class Timeline(AuthTokenPageMixin, Page):

    parent_page_types = []
    subpage_types = ['gallery.Gallery']

    paginate_by = 20

    class Meta:
        db_table = 'privagal_timeline'

    def get_context(self, request, *args, **kwargs):
        context = super(Timeline, self).get_context(request, *args, **kwargs)

        search_query = request.GET.get('query', None)
        context['search_query'] = search_query

        paginator, page = self.get_galleries(request, search_query)
        context['page_obj'] = page
        context['object_list'] = page.object_list
        context['is_paginated'] = page.has_other_pages()

        return context

    def get_galleries(self, request, search_query):
        qs = (
            Gallery.objects
            .live()
            .prefetch_related(
                Prefetch(
                    'images',
                    queryset=ImageGallery.objects.select_related('image'),
                )
            )
            .order_by('-date')
        )

        if search_query:
            qs = qs.search(search_query, order_by_relevance=False)

        return paginate(request, qs, per_page=self.paginate_by)
