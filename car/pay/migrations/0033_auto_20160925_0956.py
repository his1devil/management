# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-25 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0032_auto_20160925_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='safe',
            name='financial',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]