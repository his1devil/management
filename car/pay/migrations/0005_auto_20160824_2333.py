# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-24 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0004_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='orderinfo',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='orders',
            name='mobile',
            field=models.CharField(default='0', max_length=50),
        ),
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=models.CharField(default='0', max_length=50),
        ),
    ]
