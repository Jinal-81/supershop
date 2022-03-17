from django.contrib import admin

# Register your models here.
from userlogin.models import MyUser, Address

admin.site.register(MyUser)
admin.site.register(Address)