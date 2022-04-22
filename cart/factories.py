import factory
from cart.models import Cart, CartItem
from product.factories import ProductFactory
from userlogin.factories import UserFactory


class CartFactory(factory.django.DjangoModelFactory):
    """
    factory for cart.
    """
    class Meta:
        model = Cart

    total_amount = 1500
    status = Cart.StatusInCart.OPEN
    user = factory.SubFactory(UserFactory)


class CartItemFactory(factory.django.DjangoModelFactory):
    """
    factory for cartItem.
    """
    class Meta:
        model = CartItem

    price = 1500
    quantity = 5
    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)