# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils.translation import get_language, to_locale

from wagtail.wagtailimages.models import get_image_model

import factory
from factory import fuzzy
from faker import Factory as FakerFactory

from privagal.core.factories import PageFactory

from .models import Gallery, ImageGallery

language = get_language() or 'en-us'
locale = to_locale(language)
faker = FakerFactory.create(locale)


class ImageFactory(factory.DjangoModelFactory):

    class Meta:
        model = get_image_model()

    title = factory.Faker('sentence', locale=locale)
    file = factory.django.ImageField()


class ImageGalleryFactory(factory.DjangoModelFactory):

    class Meta:
        model = ImageGallery

    description = factory.Faker('sentence', locale=locale)


class GalleryFactory(PageFactory):

    class Meta:
        model = Gallery

    date = fuzzy.FuzzyDate(datetime.date(2016, 1, 1))
    body = factory.LazyAttribute(
        lambda x: "<p>{}</p>".format(faker.paragraph()))

    @factory.post_generation
    def images(self, created, extracted, **kwargs):
        """
        Usage example:
        >>> GalleryFactory(images__images=[ImageFactory()])
        """
        images = kwargs.pop('images', [])
        if not images:
            images = [ImageFactory() for i in range(0, 3)]

        self.images = [ImageGalleryFactory.build(page=self, image=i) for i in images]
