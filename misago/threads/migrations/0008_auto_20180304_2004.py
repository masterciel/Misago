# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-04 20:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misago_threads', '0007_auto_20171008_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='misago_threads.Post'),
        ),
        migrations.AddField(
            model_name='thread',
            name='answer_is_protected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='thread',
            name='answer_set_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
