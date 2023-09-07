# Generated by Django 4.2.4 on 2023-09-04 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
        ('photos', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='photos_album', to='albums.album'),
        ),
    ]