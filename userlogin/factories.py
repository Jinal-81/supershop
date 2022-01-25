import factory
from django.contrib.auth import get_user_model
from .models import MyUser
import datetime


class UserFactory(factory.django.DjangoModelFactory):
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
