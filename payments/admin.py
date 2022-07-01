from django.contrib import admin

# Register your models here.
from payments.models import Transaction

admin.site.register(Transaction)