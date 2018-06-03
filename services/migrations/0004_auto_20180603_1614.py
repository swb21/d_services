# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-03 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20180603_1422'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dormitory',
            options={
                'ordering': ['number'],
                'verbose_name': 'Dormitory',
                'verbose_name_plural': 'Dormitories'
            },
        ),
        migrations.AlterModelOptions(
            name='washingmachine',
            options={
                'ordering': ['-is_exploitable', 'dormitory__number', 'number'],
                'verbose_name': 'Washing machine',
                'verbose_name_plural': 'Washing machines'
            },
        ),
    ]
