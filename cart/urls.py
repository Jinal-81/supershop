# cart/urls.py
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views
from .api import CartViewSet, CartItemViewSet

router = DefaultRouter()  # router for the cart and cart item.
router.register(r'cart-api', CartViewSet, basename='cart-list')
router.register(r'cartitems', CartItemViewSet, basename='cartitem-list')

urlpatterns = [
    path('/cartview/', views.cart, name='cart'),
    path('cartitem_remove/<int:id>', views.cart_item_remove, name='cartitem_remove'),
    path('/cartitem_update/<int:id>', views.cart_item_update, name='cartitem_update'),
    path('/order/', views.order, name='order'),
    # path('/success/', TemplateView.as_view(template_name="order.html"), name="success")

]

urlpatterns += router.urls
