# Generated by Django 2.2 on 2019-04-22 19:26

import cartoview.base_resource.models
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='No title Provided', max_length=255)),
                ('description', models.TextField(blank=True, default='No Description Provided', null=True)),
                ('abstract', models.TextField(blank=True, default='No Abstract Provided', null=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to=cartoview.base_resource.models.thumbnail_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=cartoview.base_resource.models.thumbnail_path)),
            ],
            options={
                'ordering': ('title', '-created_at', '-updated_at'),
            },
        ),
        migrations.CreateModel(
            name='TaggedResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tagged_items', to='base_resource.BaseModel')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_resource_taggedresource_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='basemodel',
            name='keywords',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='base_resource.TaggedResource', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
