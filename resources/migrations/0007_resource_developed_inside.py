# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-30 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0006_resource_resource_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='developed_inside',
            field=models.BooleanField(default=False),
        ),
    ]
