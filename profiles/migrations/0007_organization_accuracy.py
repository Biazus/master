# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-25 14:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20180314_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='accuracy',
            field=models.FloatField(blank=True, null=True, verbose_name='Accuracy'),
        ),
    ]
