from datetime import time

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.versioning import QueryParameterVersioning

from cart.models import CartItem, Cart
from cart.serializer import CartSerializer, CartSerializerV1, CartItemSerializer, CartItemSerializerV2
from cart.views import cart_logger

CART_ITEM_V2_LOG_MSG = "cart item serializer v2 called with status field only."
CART_ITEM_V1_LOG_MSG = "cart item serializer v1 called with all the fields."
CART_V2_LOG_MSG = "cart serializer v2 called with cart and product fields."
CART_V1_LOG_MSG = "cart serializer v1 called with all the fields"


class CustomNumberPagination(PageNumberPagination):
    """api for the pagination."""
    page_size = 10  # Put the number of items you want in one page


class CartViewSet(viewsets.ModelViewSet):
    """API for the cart using modelViewSet for view and edit products."""
    versioning_class = QueryParameterVersioning  # request.version It will be worth it
    pagination_class = CustomNumberPagination  # set pagination class.
    queryset = Cart.objects.filter(status=Cart.StatusInCart.OPEN)  # fetch cart according open status.
    serializer_class = CartSerializer  # call serializer for the cart
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id', ]  # filter according id.
    # lookup_field = 'id'
    # lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """get version and called serializer according version."""
        if self.request.version == 'v2':  # check version
            cart_logger.info(CART_V2_LOG_MSG)
            return CartSerializerV1  # call serializer according version.
        cart_logger.info(CART_V1_LOG_MSG)
        return CartSerializer

    # def get_validated_token(self, raw_token):
    #     import pdb; pdb.set_trace()
    #     return super(CartViewSet, self).get_validated_token(raw_token)


class CartItemViewSet(viewsets.ModelViewSet):
    """API for the cartitem using modelViewSet and router"""

    versioning_class = QueryParameterVersioning  # request.version It will be worth it
    queryset = CartItem.objects.all()  # fetch all the cart item.
    serializer_class = CartItemSerializer  # call serializer for te cart item
    pagination_class = CustomNumberPagination  # call pagination class.
    search_fields = ['cart__user__username', ]  # __ used when we search using foreign key relationship
    permission_classes = [IsAuthenticated]  # authentication required user need to log in to access this api

    def get_serializer_class(self):
        """get version and called serializer according."""
        if self.request.version == 'v2':  # check version
            cart_logger.info(CART_ITEM_V2_LOG_MSG)
            return CartItemSerializerV2  # call serializer according version.
        cart_logger.info(CART_ITEM_V1_LOG_MSG)
        return CartItemSerializer


