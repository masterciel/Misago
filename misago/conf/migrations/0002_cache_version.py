# Generated by Django 1.11.16 on 2018-12-02 15:54
from django.db import migrations

from misago.cache.operations import StartCacheVersioning

from misago.conf import SETTINGS_CACHE


class Migration(migrations.Migration):

    dependencies = [("misago_conf", "0001_initial")]

    operations = [StartCacheVersioning(SETTINGS_CACHE)]
