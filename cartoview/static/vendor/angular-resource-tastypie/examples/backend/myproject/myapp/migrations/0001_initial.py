# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 02:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('song', models.CharField(blank=True, max_length=200, null=True)),
                ('artist', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ['rank'],
            },
        ),
    ]