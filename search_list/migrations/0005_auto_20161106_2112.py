# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_list', '0004_auto_20161106_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='text',
            field=models.TextField(),
        ),
    ]
