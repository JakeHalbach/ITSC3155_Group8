# Generated by Django 5.1.7 on 2025-04-29 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_media_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='poster',
            field=models.ImageField(blank=True, default='images/jakespeople.png', null=True, upload_to='images/'),
        ),
    ]
