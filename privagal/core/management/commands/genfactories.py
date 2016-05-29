# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random

from django.conf import settings
from django.core.management.base import BaseCommand

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import get_image_model

from privagal.gallery.factories import GalleryFactory, ImageFactory
from privagal.gallery.models import Gallery
from privagal.timeline.models import Timeline

ASSETS_PATH = os.path.join(settings.PROJECT_DIR, 'core', 'tests', 'assets')
IMAGES = [
    'django.png',
    'django-pony.png',
    'django-pony-pink.jpg',
    'wagtail.png',
    'wagtail-space.png',
    'python.jpg',
]

Image = get_image_model()


class Command(BaseCommand):
    help = 'Generate some data for a demo purpose.'
    leave_locale_alone = True

    def add_arguments(self, parser):
        parser.add_argument('--limit', action='store', type=int, default=5,
                            help="How many galleries to generate")
        parser.add_argument('--purge', action='store_true', default=False,
                            help="Whether to delete all previous galleries "
                                 "before creating new ones.")

    def handle(self, *args, **options):

        if options.get('purge'):
            Page.objects.type(Gallery).delete()
            Image.objects.all().delete()

        images = []
        for image in IMAGES:
            images.append(
                ImageFactory(file__from_path=os.path.join(ASSETS_PATH, image)))

        timeline = Timeline.objects.last()
        for i in range(0, options['limit']):
            random.shuffle(images)
            gallery = GalleryFactory(images__images=images)
            timeline.add_child(instance=gallery)

        self.stdout.write(
            'Galleries have been generated successfully.',
            style_func=self.style.MIGRATE_SUCCESS,
        )
