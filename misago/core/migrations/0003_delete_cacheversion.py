# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-08 19:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('misago_core', '0002_basic_settings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CacheVersion',
        ),
    ]
