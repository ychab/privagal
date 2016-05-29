# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import zipfile

from django.conf import settings
from django.db import models
from django.template import loader
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import PAGE_TEMPLATE_VAR, Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import get_image_model

from modelcluster.fields import ParentalKey
from sendfile import sendfile

from privagal.core.mixins import AuthTokenPageMixin


class Gallery(AuthTokenPageMixin, Page):
    date = models.DateField("Post date", default=timezone.now)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body', classname="full"),
        InlinePanel('images', label=_('Images')),
    ]

    parent_page_types = ['timeline.Timeline']
    subpage_types = []

    class Meta:
        db_table = 'privagal_gallery'
        verbose_name = _("Gallery")

    @property
    def image_teaser(self):
        return self.images.first()

    @property
    def teaser(self):
        return loader.render_to_string(
            'gallery/gallery_teaser.html',
            {
                PAGE_TEMPLATE_VAR: self,
            },
        )

    def serve_download(self, request):
        file = self._get_archive()
        return sendfile(request, file.filename, attachment=True)

    def _get_archive(self):
        directory = os.path.join(settings.MEDIA_ROOT, 'archives')
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(
            directory, '{gallery.date}-{gallery.pk}.zip'.format(gallery=self))
        # Force the moment, don't use cache but recreate it each time. Anyway,
        # store it in global private directory to be served by sendfile.
        return self._generate_zipfile(filepath)

    def _generate_zipfile(self, filepath):
        zf = zipfile.ZipFile(filepath, mode='w')
        for image in self.images.all().prefetch_related('image'):
            zf.write(
                image.image.file.path, os.path.basename(image.image.file.name))
        zf.close()
        return zf


class ImageGallery(Orderable):
    page = ParentalKey(Gallery, related_name='images')
    image = models.ForeignKey(
        get_image_model(),
        related_name='images_gallery'
    )
    description = models.TextField(default='', blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('description'),
    ]
