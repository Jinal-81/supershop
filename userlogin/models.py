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
    objects = None  # this is for objects variable because I am getting warning in view for objects.
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True, null=True)
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6)
    landmark = models.CharField(max_length=25)
    state = models.CharField(max_length=10)
    address_type = models.CharField(max_length=20)

    class Meta:
        """
        both the fields unique.
        """
        unique_together = [
            ["zipcode", "landmark", "user"],
        ]

    def __str__(self):
        """
        show the object name in string format.
        """
        return self.landmark