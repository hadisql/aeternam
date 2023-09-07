# Generated by Django 4.2.4 on 2023-09-06 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.AddField(
            model_name='customuser',
            name='hide_connections',
            field=models.BooleanField(default=False),
        ),
    ]