# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-04 21:41
from __future__ import unicode_literals

from django.db import migrations


ATTACHMENTS = [
    {
        'name': 'GIF',
        'extensions': ('gif', ),
        'mimetypes': ('image/gif', ),
        'size_limit': 5 * 1024
    },
    {
        'name': 'JPG',
        'extensions': ('jpg', 'jpeg', ),
        'mimetypes': ('image/jpeg', ),
        'size_limit': 3 * 1024
    },
    {
        'name': 'PNG',
        'extensions': ('png', ),
        'mimetypes': ('image/png', ),
        'size_limit': 3 * 1024
    },
    {
        'name': 'PDF',
        'extensions': ('pdf', ),
        'mimetypes': ('application/pdf', 'application/x-pdf', 'application/x-bzpdf', 'application/x-gzpdf',),
        'size_limit': 4 * 1024
    },
    {
        'name': 'Text',
        'extensions': ('txt', ),
        'mimetypes': ('text/plain', ),
        'size_limit': 4 * 1024
    },
    {
        'name': 'Markdown',
        'extensions': ('md', ),
        'mimetypes': ('text/markdown', ),
        'size_limit': 4 * 1024
    },
    {
        'name': 'reStructuredText',
        'extensions': ('rst', ),
        'mimetypes': ('text/x-rst', ),
        'size_limit': 4 * 1024
    },
    {
        'name': '7Z',
        'extensions': ('7z', ),
        'mimetypes': ('application/x-7z-compressed', ),
        'size_limit': 4 * 1024
    },
    {
        'name': 'RAR',
        'extensions': ('rar', ),
        'mimetypes': ('application/vnd.rar', ),
        'size_limit': 4 * 1024
    },
    {
        'name': 'TAR',
        'extensions': ('tar', ),
        'mimetypes': ('application/x-tar', ),
        'size_limit': 4 * 1024
    },
    {
        'name': 'GZ',
        'extensions': ('gz', ),
        'mimetypes': ('application/gzip', ),
        'size_limit': 4 * 1024
    },
    {
        'name': 'ZIP',
        'extensions': ('zip', 'zipx', ),
        'mimetypes': ('application/zip', ),
        'size_limit': 4 * 1024
    },
]


def create_attachment_types(apps, schema_editor):
    AttachmentType = apps.get_model('misago_threads', 'AttachmentType')
    for attachment in ATTACHMENTS:
        kwargs = attachment
        kwargs['extensions'] = ','.join(kwargs['extensions'])
        kwargs['mimetypes'] = ','.join(kwargs['mimetypes'])
        AttachmentType.objects.create(**kwargs)


class Migration(migrations.Migration):

    dependencies = [
        ('misago_threads', '0002_threads_settings'),
    ]

    operations = [
        migrations.RunPython(create_attachment_types),
    ]
