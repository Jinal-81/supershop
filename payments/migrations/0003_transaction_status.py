# Generated by Django 4.0.1 on 2022-06-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_remove_transaction_created_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('CANCEL', 'Cancel')], default='PENDING', max_length=15),
        ),
    ]
