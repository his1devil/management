# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-22 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('group', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
                ('note', models.CharField(max_length=128)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
