# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-25 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homes', '0010_banner_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='label',
            field=models.CharField(default='A', max_length=50),
            preserve_default=False,
        ),
    ]
