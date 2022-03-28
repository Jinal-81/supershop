from django.contrib import admin
from cart.models import Cart, CartItem
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'status')
    list_filter = ('total_amount', 'status')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)