# Generated by Django 4.2.4 on 2023-09-05 14:23

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_customuser_premium_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=sorl.thumbnail.fields.ImageField(blank=True, default='profile_pictures/default.jpg', upload_to='profile_pictures/', verbose_name='profile picture'),
        ),
    ]