# Generated by Django 4.0.1 on 2022-03-01 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0017_remove_productcartitem_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
