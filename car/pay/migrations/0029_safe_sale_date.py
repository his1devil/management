# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-04 03:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0028_safe_pos_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='safe',
            name='sale_date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 9, 4, 3, 49, 5, 379456, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
