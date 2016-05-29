# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from privagal.timeline.models import Timeline

from .models import Token


class AuthTokenMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        key = request.GET.get('token', None)
        if key is None:
            return

        try:
            Token.objects.get(key=key)
        except Token.DoesNotExist:
            pass
        else:
            page = Timeline.objects.get(slug='timeline')
            restrictions = page.get_view_restrictions()
            # If password changes, we need to update new restrictions.
            request.session['passed_page_view_restrictions'] = [
                r.id for r in restrictions]
