from django.db import models
from django.utils.translation import gettext_lazy as _

from product.models import Product
from userlogin.models import MyUser


# Create your models here.
class Cart(models.Model):
    """
    create Cart table for products.
    """
    class StatusInCart(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        PLACED = 'PLACED', _('Placed')

    objects = None
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=False)
    total_amount = models.FloatField(default=0, null=True)
    status = models.CharField(max_length=10, choices=StatusInCart.choices, default=StatusInCart.OPEN)  # open or placed

    class Meta:
        ordering = ['id']

    def __str__(self):
        """
        show the object name in string format.
        """
        return self.user.username


class CartItem(models.Model):
    """
    create cart item table for cart
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=False, related_name='usercart')
    quantity = models.IntegerField(default=1, null=False)
    price = models.FloatField(default=0, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """
        show the object name in string format.
        """
        return self.product.name