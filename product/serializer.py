from rest_framework import serializers
from product.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    """
    serializer for the product.
    """
    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerV1(serializers.ModelSerializer):
    """
    serializer for the product name only using versioning.
    """
    class Meta:
        model = Product
        fields = ('name', )


class CategorySerializer(serializers.ModelSerializer):
    """
    serializer for the category
    """
    class Meta:
        model = Category
        fields = '__all__'


