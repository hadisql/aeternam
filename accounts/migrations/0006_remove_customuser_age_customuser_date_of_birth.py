# Generated by Django 4.2.2 on 2023-08-08 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='age',
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]