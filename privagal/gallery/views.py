# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.views.generic import View

from privagal.core.mixins import PageLoginRequiredMixin

from .models import Gallery


class GalleryDownloadView(PageLoginRequiredMixin, View):

    def get(self, request, pk):
        gallery = get_object_or_404(Gallery, pk=pk)
        return gallery.serve_download(request)
