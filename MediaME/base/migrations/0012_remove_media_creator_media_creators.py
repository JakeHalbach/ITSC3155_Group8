# Generated by Django 5.1.6 on 2025-04-08 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_media_creators_media_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='creator',
        ),
        migrations.AddField(
            model_name='media',
            name='creators',
            field=models.ManyToManyField(blank=True, related_name='created_media', to='base.creator'),
        ),
    ]
