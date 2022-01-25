from django.contrib import admin

# Register your models here.
from userlogin.models import MyUser

admin.site.register(MyUser)