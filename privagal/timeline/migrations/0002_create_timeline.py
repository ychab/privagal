# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def create_timeline(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    PageViewRestriction = apps.get_model('wagtailcore.PageViewRestriction')
    Site = apps.get_model('wagtailcore.Site')
    Timeline = apps.get_model('timeline.Timeline')

    # Delete the default homepage
    Page.objects.get(id=2).delete()

    content_type, created = ContentType.objects.get_or_create(
        model='timeline', app_label='timeline')

    timeline = Timeline.objects.create(
        title="Timeline",
        slug='timeline',
        content_type=content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/timeline/',
    )

    PageViewRestriction.objects.create(
        page=timeline, password=settings.PRIVAGAL_TIMELINE_INITIAL_PASSWORD)

    Site.objects.create(
        hostname=settings.PRIVAGAL_SITE_HOSTNAME,
        root_page=timeline,
        is_default_site=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_timeline),
    ]
