# Generated by Django 4.2.2 on 2023-07-29 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(choices=[('UNDEFINED', 'UNDEFINED'), ('SIBLING', 'SIBLING'), ('PARENT/CHILDREN', 'PARENT/CHILDREN'), ('COUSIN', 'COUSIN'), ('AUNT-UNCLE/NEPHEW-NIECE', 'AUNT-UNCLE/NEPHEW-NIECE'), ('GRANDPARENT/GRANDCHILDREN', 'GRANDPARENT/GRANDCHILDREN'), ('BROTHER/SISTER IN LAW', 'BROTHER/SISTER IN LAW'), ('FRIEND', 'FRIEND')], default='UNDEFINED', max_length=50)),
                ('user_receiving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation_req_receiver', to=settings.AUTH_USER_MODEL)),
                ('user_sending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation_req_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_receiving', 'user_sending')},
            },
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(choices=[('UNDEFINED', 'UNDEFINED'), ('SIBLING', 'SIBLING'), ('PARENT/CHILDREN', 'PARENT/CHILDREN'), ('COUSIN', 'COUSIN'), ('AUNT-UNCLE/NEPHEW-NIECE', 'AUNT-UNCLE/NEPHEW-NIECE'), ('GRANDPARENT/GRANDCHILDREN', 'GRANDPARENT/GRANDCHILDREN'), ('BROTHER/SISTER IN LAW', 'BROTHER/SISTER IN LAW'), ('FRIEND', 'FRIEND')], default='UNDEFINED', max_length=50)),
                ('user_receiving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation_receiver', to=settings.AUTH_USER_MODEL)),
                ('user_sending', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_receiving', 'user_sending')},
            },
        ),
    ]
