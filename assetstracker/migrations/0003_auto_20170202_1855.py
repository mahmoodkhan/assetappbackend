# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-02 18:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assetstracker', '0002_auto_20170202_1824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='asset_type',
            new_name='assettype',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='po_number',
            new_name='ponumber',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='pr_number',
            new_name='prnumber',
        ),
    ]
