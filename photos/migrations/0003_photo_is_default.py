# Generated by Django 4.2.2 on 2023-07-24 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_remove_photo_uploader_remove_photo_url_photo_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
