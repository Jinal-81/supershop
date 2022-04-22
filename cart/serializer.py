from rest_framework import serializers
from cart.models import Cart, CartItem


class CartSerializerV1(serializers.ModelSerializer):
    """
    serializer for the cart using versioning.
    """
    class Meta:
        model = Cart
        fields = ['status', ]


class CartItemSerializer(serializers.ModelSerializer):
    """
    serializer for the cart item.
    """
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    """
    serializer for the cart.
    """
    usercart = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializerV2(serializers.ModelSerializer):
    """
    serializer for the cart item.
    """
    class Meta:
        model = CartItem
        fields = ['cart', 'product', ]

