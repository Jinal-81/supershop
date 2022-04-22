from django.db import models


# Create your models here.
class Category(models.Model):
    """
    create categories.
    """
    objects = None
    name = models.CharField(max_length=50)
    category = models.ManyToManyField("self", blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """
        show the object name in string format.
        """
        return self.name


class Product(models.Model):
    """
    Create Product table for Products.
    """
    objects = None
    name = models.CharField(max_length=60)
    price = models.FloatField()
    description = models.CharField(max_length=1000)
    product_image = models.ImageField(upload_to='images/')
    quantity = models.IntegerField(default=0, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """
        show the object name in string format.
        """
        return self.name