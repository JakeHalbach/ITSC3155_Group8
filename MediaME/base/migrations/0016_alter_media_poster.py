# Generated by Django 5.1.7 on 2025-04-08 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_alter_media_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='poster',
            field=models.ImageField(blank=True, default='../images/images/spongeboy.jpg', null=True, upload_to='images/'),
        ),
    ]
