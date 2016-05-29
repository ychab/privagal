# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'db_table': 'privagal_token',
                'get_latest_by': 'created',
            },
        ),
    ]
