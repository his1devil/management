# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-22 10:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0002_auto_20160822_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='role',
        ),
    ]
