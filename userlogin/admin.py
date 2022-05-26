from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from userlogin.models import MyUser, Address

admin.site.register(MyUser, UserAdmin)
admin.site.register(Address)