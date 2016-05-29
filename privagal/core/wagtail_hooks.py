# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.wagtailadmin.widgets import Button
from wagtail.wagtailcore import hooks

from privagal.gallery.models import Gallery
from privagal.timeline.models import Timeline

from .models import Token
from .views import TokenCreateView


@hooks.register('register_page_listing_more_buttons')
def page_listing_button_link_token(page, page_perms, is_parent):
    if not isinstance(page, (Timeline, Gallery)):
        return

    token = Token.objects.singleton()
    if token:
        yield Button(
            _('Token link'),
            '{url}?token={key}'.format(url=page.full_url, key=token.key),
            attrs={'title': _('Copy this link address to share it.')},
            priority=0
        )


class TokenAdmin(ModelAdmin):
    model = Token
    menu_label = _('Token')
    menu_icon = 'password'
    add_to_settings_menu = True
    list_display = ('key', 'created')
    ordering = ('-created',)
    create_view_class = TokenCreateView

modeladmin_register(TokenAdmin)
