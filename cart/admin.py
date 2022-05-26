from django.contrib import admin

from cart.models import Cart, CartItem


# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'status')  # fields display
    list_filter = ('total_amount', 'status')    # fields for the filter
    search_fields = ('total_amount', 'status')  # fields for the search


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)