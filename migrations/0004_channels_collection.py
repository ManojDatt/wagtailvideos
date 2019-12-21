# Generated by Django 2.2.8 on 2019-12-21 09:21

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailvideos', '0003_auto_20191221_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='channels',
            name='collection',
            field=models.ForeignKey(default=wagtail.core.models.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Collection', verbose_name='collection'),
        ),
    ]