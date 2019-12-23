# Generated by Django 2.2.8 on 2019-12-21 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumchoicefield.fields
import taggit.managers
import wagtail.core.models
import wagtail.search.index
import wagtailvideos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Channel',
                'verbose_name_plural': 'Channels',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.FileField(upload_to=wagtailvideos.models.get_upload_to, verbose_name='file')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=wagtailvideos.models.get_upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('duration', models.DurationField(blank=True, null=True)),
                ('scope', models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], default='PUBLIC', max_length=30, verbose_name='Scope')),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wagtailvideos.Channels', verbose_name='Channel')),
                ('collection', models.ForeignKey(default=wagtail.core.models.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Collection', verbose_name='collection')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='VideoTranscode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_format', enumchoicefield.fields.EnumChoiceField(enum_class=wagtailvideos.models.MediaFormats, max_length=4)),
                ('quality', enumchoicefield.fields.EnumChoiceField(default=wagtailvideos.models.VideoQuality(1), enum_class=wagtailvideos.models.VideoQuality, max_length=7)),
                ('processing', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to=wagtailvideos.models.get_upload_to, verbose_name='file')),
                ('error_message', models.TextField(blank=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transcodes', to='wagtailvideos.Video')),
            ],
            options={
                'unique_together': {('video', 'media_format')},
            },
        ),
    ]
