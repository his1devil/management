# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-01 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0017_auto_20160902_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploaded',
            name='vin',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
