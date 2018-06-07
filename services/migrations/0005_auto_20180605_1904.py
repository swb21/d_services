# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-05 16:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20180603_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='WashingTime',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('time', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='washingschedule',
            name='washing_time',
        ),
        migrations.AddField(
            model_name='washingschedule',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='washingschedule',
            name='time',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='services.WashingTime'),
        ),
    ]
