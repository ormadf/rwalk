# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-29 01:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='text',
            field=models.CharField(max_length=200),
        ),
    ]