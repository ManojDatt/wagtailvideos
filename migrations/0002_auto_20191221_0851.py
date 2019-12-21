# Generated by Django 2.2.8 on 2019-12-21 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailvideos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wagtailvideos.Channels', verbose_name='Channel'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='title'),
        ),
    ]
