# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-25 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0031_auto_20160923_2302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='email',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='fax',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='urgent_mobile',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='urgent_name',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='urgent_phone',
        ),
        migrations.RemoveField(
            model_name='safe',
            name='car_date',
        ),
        migrations.RemoveField(
            model_name='safe',
            name='safe_date',
        ),
        migrations.AddField(
            model_name='safe',
            name='second_equip_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='safe',
            name='writer',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='safe',
            name='car_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
