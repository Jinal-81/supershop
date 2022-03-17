# Usersite/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('category_search/<int:id>', views.category_search, name='category_search'),
    path('login/', views.view_login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', LogoutView.as_view(template_name='userlogin/Homepage.html'), name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('profile/', views.user_profile, name='profile'),
    path('address/', views.user_address, name='user_address'),
    path('remove_address/', views.remove_address, name='remove_address'),
    path('user_address_update/', views.user_addresses_update, name='user_address_update')
]