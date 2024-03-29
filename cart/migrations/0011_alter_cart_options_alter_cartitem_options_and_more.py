# Generated by Django 4.0.1 on 2022-04-20 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='usercart', to='cart.cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
