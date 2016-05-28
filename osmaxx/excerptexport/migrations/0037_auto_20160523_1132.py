# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 09:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('excerptexport', '0036_move_download_files_to_new_field_20160520_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='export',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now, editable=False, verbose_name='created at'),
        ),
        migrations.AddField(
            model_name='export',
            name='finished_at',
            field=models.DateTimeField(blank=True, default=None, editable=False, null=True, verbose_name='finished at'),
        ),
        migrations.AddField(
            model_name='export',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=None, editable=False, null=True, verbose_name='updated at'),
        ),
    ]