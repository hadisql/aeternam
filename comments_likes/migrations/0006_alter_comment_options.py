# Generated by Django 4.2.4 on 2023-08-24 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments_likes', '0005_alter_comment_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
    ]