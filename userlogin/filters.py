import django_filters

from product.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # filter if abc jacket and if user entered only abc then

    class Meta:
        model = Product
        fields = ['name']