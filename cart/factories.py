import factory
from cart.models import Cart, CartItem


class CartFactory(factory.django.DjangoModelFactory):
    """
    factory for cart.
    """
    class Meta:
        model = Cart

    total_amount = 1500
    status = Cart.StatusInCart.OPEN


class CartItemFactory(factory.django.DjangoModelFactory):
    """
    factory for cart.
    """
    class Meta:
        model = CartItem

    price = 1500
    quantity = 5
    cart = factory.SubFactory(CartFactory)