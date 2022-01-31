from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class MyUser(AbstractUser):
    """
    create user registration model using abstract user
    """
    mobile_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='images/')


class Address(models.Model):
    """
    create address for user.
    """
    objects = None
    MyUser_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6)
    landmark = models.CharField(max_length=25)
    state = models.CharField(max_length=10)
