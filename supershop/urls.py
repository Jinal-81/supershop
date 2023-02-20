"""supershop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from userlogin.api import LoginAPIView

admin.site.site_header = "SuperShop Administration"
admin.site.site_title = "Super Shop Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userlogin.urls')),
    path('product', include('product.urls')),
    path('payment', include('payments.urls')),
    re_path(r'^api/v5', include(('product.urls', 'product'), namespace='v5')),
    re_path(r'^api/(v1|v2|v5)', include(('product.urls', 'product'), namespace='v2')),
    path('cart', include('cart.urls')),
    re_path(r'^api/', include(('cart.urls', 'cart'), namespace='cart')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='userlogin/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="userlogin/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='userlogin/password/password_reset_complete.html'), name='password_reset_complete'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
router.register('user', LoginAPIView, basename='user')  # for the login view.

urlpatterns += router.urls