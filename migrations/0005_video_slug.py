# Generated by Django 2.2.8 on 2019-12-21 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailvideos', '0004_channels_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
