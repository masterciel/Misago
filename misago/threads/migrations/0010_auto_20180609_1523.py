# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-09 15:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('misago_threads', '0009_auto_20180326_0010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='uploader_ip',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='poster_ip',
        ),
        migrations.RemoveField(
            model_name='pollvote',
            name='voter_ip',
        ),
        migrations.RemoveField(
            model_name='post',
            name='poster_ip',
        ),
        migrations.RemoveField(
            model_name='postedit',
            name='editor_ip',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='liker_ip',
        ),
    ]
