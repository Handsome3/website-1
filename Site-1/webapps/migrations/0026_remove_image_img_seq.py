# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-17 15:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('webapps', '0025_auto_20170615_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='img_seq',
        ),
    ]