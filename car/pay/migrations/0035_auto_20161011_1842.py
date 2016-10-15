# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-11 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0034_safe_b_care_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareNu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_care_number', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='safe',
            name='b_care_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pay.CareNu'),
        ),
    ]
