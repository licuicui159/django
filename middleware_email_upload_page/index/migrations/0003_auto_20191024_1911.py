# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-10-24 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_emailuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailuser',
            name='eaddr',
            field=models.EmailField(max_length=11, verbose_name='email地址'),
        ),
    ]