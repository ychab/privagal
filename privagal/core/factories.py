# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import get_language, to_locale

from wagtail.wagtailcore.models import Page

import factory

from .models import Token

language = get_language() or 'en-us'
locale = to_locale(language)


class PageFactory(factory.DjangoModelFactory):
    """
    Page factory may not be created directly and thus, the default strategy
    is forced to BUILD. To save it, you MUST to do it with a parent page.
    Typically, you need a parent page instance and apply add_child() method:
    >>> PageParent.add_child(instance=MyPageFactory())
    <MyPage: Dolorem rem assumenda modi eum.>
    """

    class Meta:
        abstract = True
        strategy = factory.BUILD_STRATEGY

    title = factory.Faker('sentence', locale=locale)
    slug = factory.LazyAttributeSequence(
        lambda o, n: '{type}_{n}'.format(
            type=o._LazyStub__model_class._meta.model.__name__.lower(),
            n=n,
        )
    )

    @classmethod
    def _setup_next_sequence(cls):
        """
        Returns the last ID for persistant sequence (used by slug and so on).

        IMPORTANT: we should always have pages, at least root and timeline.
        """
        return (
            Page.objects
            .values('pk')
            .order_by('-pk')[:1]
        )[0]['pk'] + 1


class TokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = Token
