# Generated by Django 4.0.1 on 2022-06-06 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0022_alter_address_options_alter_myuser_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='code1',
            field=models.IntegerField(default=1),
        ),
    ]
