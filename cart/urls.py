# cart/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('/cart/', views.cart, name='cart'),
    path('cartitem_remove/<int:id>', views.cart_item_remove, name='cartitem_remove'),
    path('cartitem_update/<int:id>', views.cart_item_update, name='cartitem_update'),
    path('/order/', views.order, name='order'),
    path('view_order_list/', views.view_order_list, name='view_order_list'),
]