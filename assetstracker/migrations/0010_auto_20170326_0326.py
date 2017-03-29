# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-26 03:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assetstracker', '0009_auto_20170322_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assetissuancehistory',
            name='item',
        ),
        migrations.AddField(
            model_name='assetissuancehistory',
            name='asset',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='asset_history', to='assetstracker.Asset'),
            preserve_default=False,
        ),
    ]