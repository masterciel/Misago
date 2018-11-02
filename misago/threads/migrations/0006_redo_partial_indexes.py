# Generated by Django 1.11.1 on 2017-05-21 17:52
import django.contrib.postgres.indexes
from django.contrib.postgres.operations import BtreeGinExtension
from django.db import migrations

import misago.core.pgutils


class Migration(migrations.Migration):

    dependencies = [
        ('misago_threads', '0005_index_search_document'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='post',
            index=misago.core.pgutils.PgPartialIndex(fields=['has_open_reports'], name='misago_thre_has_ope_479906_part', where={'has_open_reports': True}),
        ),
        migrations.AddIndex(
            model_name='post',
            index=misago.core.pgutils.PgPartialIndex(fields=['is_hidden'], name='misago_thre_is_hidd_85db69_part', where={'is_hidden': False}),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=misago.core.pgutils.PgPartialIndex(fields=['weight'], name='misago_thre_weight_955884_part', where={'weight': 2}),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=misago.core.pgutils.PgPartialIndex(fields=['weight'], name='misago_thre_weight_9e8f9c_part', where={'weight': 1}),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=misago.core.pgutils.PgPartialIndex(fields=['weight'], name='misago_thre_weight_c7ef29_part', where={'weight': 0}),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=misago.core.pgutils.PgPartialIndex(fields=['weight'], name='misago_thre_weight__4af9ee_part', where={'weight__lt': 2}),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=misago.core.pgutils.PgPartialIndex(fields=['has_reported_posts'], name='misago_thre_has_rep_84acfa_part', where={'has_reported_posts': True}),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=misago.core.pgutils.PgPartialIndex(fields=['has_unapproved_posts'], name='misago_thre_has_una_b0dbf5_part', where={'has_unapproved_posts': True}),
        ),
        migrations.AddIndex(
            model_name='thread',
            index=misago.core.pgutils.PgPartialIndex(fields=['is_hidden'], name='misago_thre_is_hidd_d2b96c_part', where={'is_hidden': False}),
        ),
    ]
