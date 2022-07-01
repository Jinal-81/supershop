from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('/success/', PaymentSuccessView, name='success'),
    path('/failed/', PaymentFailedView, name='failed'),
    path('/view_transaction/<int:id>', views.view_transaction, name='view_transaction'),
    path('/transaction_list/', views.transaction_list, name='transaction_list'),
    path('/create-checkout-session/<int:pk>', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('/webhook/stripe', views.stripe_webhook, name="webhook"),
]