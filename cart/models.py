from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from userlogin.models import MyUser
from product.models import Product


# Create your models here.
class Cart(models.Model):
    """
    create Cart table for products.
    """
    class StatusInCart(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        PLACED = 'PLACED', _('Placed')

    objects = None
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    total_amount = models.FloatField(default=0, null=True)
    status = models.CharField(max_length=10, choices=StatusInCart.choices, default=StatusInCart.OPEN)  # open or placed

    def __str__(self):
        """
        show the object name in string format.
        """
        return self.user.username


class CartItem(models.Model):
    """
    create cart item table for cart
    """
    objects = None
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True)
    price = models.FloatField(default=0, null=True)

    def __str__(self):
        """
        show the object name in string format.
        """
        return self.product.name