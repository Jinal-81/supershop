from rest_framework import viewsets, status, generics
from rest_framework.pagination import PageNumberPagination
from product.serializer import ProductSerializer, CategorySerializer, ProductSerializerV1
from product.models import Product, Category
from rest_framework import filters


class CustomNumberPagination(PageNumberPagination):
    page_size = 10  # Put the number of items you want in one page


class ProductApi(viewsets.ModelViewSet):
    """
    API for the product using modelViewSet for view and edit products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomNumberPagination
    ordering = ['id']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_serializer_class(self):
        """
        get version and called serializer according version.
        """
        if self.request.version == 'v5':
            return ProductSerializerV1
        return ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API for the category using modelViewSet and router
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



