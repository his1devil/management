# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-19 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0038_auto_20161019_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='safe',
            name='uid',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]