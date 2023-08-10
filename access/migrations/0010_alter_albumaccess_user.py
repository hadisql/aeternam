# Generated by Django 4.2.2 on 2023-08-01 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('access', '0009_remove_albumaccess_has_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumaccess',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='album_accesses', to=settings.AUTH_USER_MODEL),
        ),
    ]