# Generated by Django 4.0.1 on 2022-03-01 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0011_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_amount',
            field=models.FloatField(null=True),
        ),
    ]
