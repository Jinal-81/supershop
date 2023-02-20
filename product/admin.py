from django.contrib import admin

from product.models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    # fields = ['name', 'price', 'description']
    fieldsets = [
        ('Product Name', {'fields': ['name'], 'classes': ['collapse']}),
        ('Product Price', {'fields': ['price'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'price', 'category')
    list_display_links = ('name', 'price') # by default first column is the list display link but we can customize or give another field as an link for the edit that record.
    list_filter = ('name', 'price', 'category__name')  # filter by the fields.
    list_select_related = ['category']
    list_per_page = 2  # list per page.
    search_fields = ('name', 'price') # searc

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)