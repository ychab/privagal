# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import get_language, to_locale

import factory
from faker import Factory as FakerFactory

from privagal.core.factories import PageFactory

from .models import Timeline

language = get_language() or 'en-us'
locale = to_locale(language)
faker = FakerFactory.create(locale)


class TimelineFactory(PageFactory):

    class Meta:
        model = Timeline

    @factory.post_generation
    def create(self, created, extracted, **kwargs):
        """
        Timeline doesn't really need a known parent but only the root page so
        BUILD_STRATEGY isn't really required. Anyway, this is more simple to
        achieve it in that way (instead of setting CREATE_STRATEGY and playing
        with a lazy path attribute and MP tree...)
        """
        if extracted is False:
            return
        root = self.get_first_root_node()
        root.add_child(instance=self)

    @factory.post_generation
    def galleries(self, created, extracted, **kwargs):
        galleries = extracted or []
        for gallery in galleries:
            self.add_child(instance=gallery)
