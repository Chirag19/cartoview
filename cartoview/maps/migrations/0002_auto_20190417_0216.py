# Generated by Django 2.2 on 2019-04-17 00:16

import cartoview.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='center',
            field=cartoview.fields.ListField(default=[0, 0]),
        ),
    ]
