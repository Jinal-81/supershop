from django.db.models.aggregates import Sum
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem


@receiver(post_save, sender=CartItem)
def save_total_price(sender, instance, created, **kwargs):
    """
    create signal for the post_save method for cartitem table.
    """
    # count total amount according cartitem price and cartitem quantity and sum that all values.
    instance.cart.total_amount = instance.cart.usercart.all().aggregate(total=Sum(F('price')*F('quantity'))).get('total', 0)
    instance.cart.save()


@receiver(post_delete, sender=CartItem)
def delete_cartitem(sender, instance, **kwargs):
    """
    create signal for the cartitem delete.
    """
    # update total amount when cartitem delete from the cart.
    instance.cart.total_amount = instance.cart.total_amount - (instance.price * instance.quantity)
    instance = instance.cart.usercart.filter(id=instance.id)  # filter cartitem id
    instance.delete()  # delete filtered item from the cartitem