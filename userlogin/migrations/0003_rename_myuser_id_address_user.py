# Generated by Django 4.0.1 on 2022-02-02 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0002_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='MyUser_id',
            new_name='user',
        ),
    ]
