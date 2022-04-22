from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.versioning import QueryParameterVersioning
from cart.models import CartItem, Cart
from cart.serializer import CartSerializer, CartSerializerV1, CartItemSerializer, CartItemSerializerV2


class CustomNumberPagination(PageNumberPagination):
    page_size = 10  # Put the number of items you want in one page


class CartViewSet(viewsets.ModelViewSet):
    """
    API for the cart using modelViewSet for view and edit products.
    """
    versioning_class = QueryParameterVersioning  # request.version It will be worth it
    pagination_class = CustomNumberPagination
    queryset = Cart.objects.filter(status=Cart.StatusInCart.OPEN)
    serializer_class = CartSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id', ]

    def get_serializer_class(self):
        """
        get version and called serializer according version.
        """
        if self.request.version == 'v2':
            return CartSerializerV1
        return CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    """
    API for the cartitem using modelViewSet and router
    """

    versioning_class = QueryParameterVersioning  # request.version It will be worth it
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = CustomNumberPagination
    search_fields = ['cart__user__username', ]  # __ used when we search using foreign key relationship

    def get_serializer_class(self):
        """
        get version and called serializer according.
        """
        if self.request.version == 'v2':
            return CartItemSerializerV2
        return CartItemSerializer


