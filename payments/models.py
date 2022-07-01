from django.db import models

from cart.models import Cart
from userlogin.models import MyUser


# Create your models here.


class Transaction(models.Model):
    """Transaction model for the payment."""

    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    CANCEL = 'CANCEL'

    STATUS_IN_TRANSACTION_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (CANCEL, 'Cancel'),
    ]

    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(to=Cart, verbose_name='Cart', on_delete=models.PROTECT)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=False)
    amount = models.IntegerField(verbose_name='Amount')
    date = models.DateField(null=True, blank=True)
    # stripe_id = models.IntegerField(default=1)
    stripe_id = models.SlugField(max_length=255)
    status = models.CharField(max_length=15, choices=STATUS_IN_TRANSACTION_CHOICES, default=PENDING)

