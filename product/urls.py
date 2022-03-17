# cart/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('/view_product/<int:id>', views.view_product, name='view_product'),
    path('/add_to_cart/<int:id>', views.view_product, name='add_to_cart')
]