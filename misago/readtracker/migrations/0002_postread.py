# Generated by Django 1.11.5 on 2017-10-07 14:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('misago_categories', '0006_moderation_queue_roles'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('misago_threads', '0006_redo_partial_indexes'),
        ('misago_readtracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_read_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='misago_categories.Category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='misago_threads.Post')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='misago_threads.Thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
