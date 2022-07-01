import datetime

import factory
from django.contrib.auth import get_user_model

from userlogin.models import Address


class UserFactory(factory.django.DjangoModelFactory):
    """
    factory for user.
    """
    class Meta:
        model = get_user_model()

    username = 'abc'
    password = 'abc'
    first_name = 'abc'
    last_name = 'desai'
    email = 'jinal@gmail.com'
    mobile_number = '7984842865'
    birth_date = datetime.date.today()
    profile_pic = 'images/girl1.jpg'
    code1 = 67706


class AddressFactory(factory.django.DjangoModelFactory):
    """
    factory for address.
    """
    class Meta:
        model = Address

    city = 'Ahmedabad'
    zipcode = '387100'
    landmark = 'PK'
    state = 'Gujarat'
    address_type = 'home'