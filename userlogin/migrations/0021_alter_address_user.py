# Generated by Django 4.0.1 on 2022-04-18 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0020_alter_address_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
