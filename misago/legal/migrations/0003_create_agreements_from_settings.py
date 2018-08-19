# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-16 14:22
from __future__ import unicode_literals

from django.db import migrations

from misago.conf.migrationutils import migrate_settings_group
from misago.legal.models import Agreement as MisagoAgreement


_ = lambda s: s


LEGAL_SETTINGS = [
    'terms_of_service_title',
    'terms_of_service_link',
    'terms_of_service',
    'privacy_policy_title',
    'privacy_policy_link',
    'privacy_policy',
]


def create_legal_settings_group(apps, schema_editor):
    Agreement = apps.get_model('misago_legal', 'Agreement')
    Setting = apps.get_model('misago_conf', 'Setting')
    
    legal_conf = {}
    for setting in Setting.objects.filter(setting__in=LEGAL_SETTINGS):
        legal_conf[setting.setting] = setting.dry_value

    if legal_conf['terms_of_service'] or legal_conf['terms_of_service_link']:
        Agreement.objects.create(
            type=MisagoAgreement.TYPE_TOS,
            title=legal_conf['terms_of_service_title'],
            link=legal_conf['terms_of_service_link'],
            text=legal_conf['terms_of_service'],
            is_active=True,
        )

    if legal_conf['privacy_policy'] or legal_conf['privacy_policy_link']:
        Agreement.objects.create(
            type=MisagoAgreement.TYPE_PRIVACY,
            title=legal_conf['privacy_policy_title'],
            link=legal_conf['privacy_policy_link'],
            text=legal_conf['privacy_policy'],
            is_active=True,
        )

    MisagoAgreement.objects.invalidate_cache()


def delete_deprecated_settings(apps, schema_editor):
    migrate_settings_group(
        apps, {
            'key': 'legal',
            'name': _("Legal information"),
            'description': _("Those settings allow you to set additional legal information for your forum."),
            'settings': [
                {
                    'setting': 'forum_footnote',
                    'name': _("Footnote"),
                    'description': _("Short message displayed in forum footer."),
                    'legend': _("Forum footer"),
                    'field_extra': {
                        'max_length': 300,
                    },
                    'is_public': True,
                },
            ],
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('misago_legal', '0002_agreement_useragreement'),
    ]

    operations = [
        migrations.RunPython(create_legal_settings_group),
        migrations.RunPython(delete_deprecated_settings),
    ]
