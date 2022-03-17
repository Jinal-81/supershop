import factory
from product.models import Product, Category


class ProductFactory(factory.django.DjangoModelFactory):
    """
    factory for product.
    """
    class Meta:
        model = Product

    name = 'ABC T-shirt'
    price = 1500
    description = 'ABC T-shirt for boys'
    product_image = 'images/GHS.jpg'
    quantity = 5


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    factory for category
    """
    class Meta:
        model = Category

    name = "T-shirt"