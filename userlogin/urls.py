# Usersite/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.view_login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('cart/', views.cart, name='cart'),
    path('view_product/', views.view_product, name='view_product'),
    path('logout/', LogoutView.as_view(template_name='userlogin/Homepage.html'), name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('profile/', views.user_profile, name='profile')
]