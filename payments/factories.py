import datetime
import random

import factory
import fake as fake
from django.contrib.auth import get_user_model
from faker import Faker

from cart.factories import CartFactory
from cart.models import Cart
from payments.models import Transaction
from userlogin.factories import UserFactory

fake = Faker()


class UserFactory1(factory.django.DjangoModelFactory):
    """
    factory for user.
    """
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    password = 'transaction1'
    first_name = 'abc'
    last_name = 'desai'
    email = 'jinal@gmail.com'
    # mobile_number =
    birth_date = datetime.date.today()
    profile_pic = 'images/girl1.jpg'
    code1 = 67706


class CartFactory1(factory.django.DjangoModelFactory):
    """
    factory for cart.
    """
    class Meta:
        model = Cart

    total_amount = 1500
    status = Cart.StatusInCart.OPEN
    # user = factory.SubFactory(UserFactory1)


class TransactionFactory(factory.django.DjangoModelFactory):
    """
    factory for Transaction.
    """
    class Meta:
        model = Transaction

    amount = 1500
    status = Transaction.PENDING
    # user = factory.SubFactory(UserFactory1)
    # cart = factory.SubFactory(CartFactory1)
    stripe_id = " "