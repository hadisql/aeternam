# Generated by Django 4.2.4 on 2023-08-24 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_notification_user_sending_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(default='Connection request', max_length=255),
            preserve_default=False,
        ),
    ]