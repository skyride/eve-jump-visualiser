# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-22 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sde', '0006_auto_20171222_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='security_class',
            field=models.CharField(max_length=2, null=True),
        ),
    ]