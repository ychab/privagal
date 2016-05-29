# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse

from wagtail.wagtailimages.views.serve import generate_signature

register = template.Library()


@register.simple_tag()
def image_url(image, filter_spec):
    signature = generate_signature(image.id, filter_spec)
    url = reverse(
        'wagtailimages_serve',
        args=(signature, image.id, filter_spec)
    )
    url += image.file.name[len('original_images/'):]
    return url
