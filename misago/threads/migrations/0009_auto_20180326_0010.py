# Generated by Django 1.11.9 on 2018-03-26 00:10
from django.db import migrations

import misago.core.pgutils


class Migration(migrations.Migration):

    dependencies = [("misago_threads", "0008_auto_20180310_2234")]

    operations = [
        migrations.AddIndex(
            model_name="post",
            index=misago.core.pgutils.PgPartialIndex(
                fields=["is_event", "event_type"],
                name="misago_thre_is_even_42bda7_part",
                where={"is_event": True},
            ),
        )
    ]
