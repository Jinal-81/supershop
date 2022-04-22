# cart/urls.py
from django.template.defaulttags import url
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views
from .api import ProductApi, CategoryViewSet

router = DefaultRouter()
router.register(r'/categories', CategoryViewSet, basename='category-list')
router.register(r'/products', ProductApi, basename='product-list')

urlpatterns = [
    path('/view_product/<int:id>', views.view_product, name='view_product'),
    path('/add_to_cart/<int:id>', views.view_product, name='add_to_cart'),
    path('/product_list/', views.product_list, name='product_list'),

]
urlpatterns += router.urls
