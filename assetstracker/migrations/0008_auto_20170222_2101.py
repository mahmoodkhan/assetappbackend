# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-22 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assetstracker', '0007_auto_20170222_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='sno1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='sno2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
