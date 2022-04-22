# Usersite/urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views, api
# actions_url = {'actions': {'get': 'list', 'post': 'create'}}
# actions_obj = {'actions': {'get': 'retrieve', 'delete': 'destroy', 'put': 'update'}}

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
    path('user_address_update/', views.user_addresses_update, name='user_address_update'),
    re_path('^api/(?P<version>(v1|v2))/user/list/', api.UserList.as_view(), name='api_user_list'),
    re_path('^api/(?P<version>(v1|v2))/user/create/', api.UserList.as_view(), name='api_user_create'),
    re_path('^api/(?P<version>(v1|v2))/user/retrieve/(?P<pk>\d+)$', api.UserDetail.as_view(), name='api_user_retrieve'),
    re_path('^api/(?P<version>(v1|v2))/user/update/(?P<pk>\d+)$', api.UserDetail.as_view(), name='api_user_update'),
    re_path('^api/(?P<version>(v1|v2))/user/delete/(?P<pk>\d+)$', api.UserDetail.as_view(), name='api_user_delete'),
    re_path('^api/(?P<version>(v1|v2))/address/list/', api.AddressList.as_view(), name='api_address_list'),
    re_path('^api/(?P<version>(v1|v2))/address/create/', api.AddressCreate.as_view(), name='api_address_create'),
    re_path('^api/(?P<version>(v1|v2))/address/retrieve/(?P<id>\d+)$', api.AddressRetrieve.as_view(), name='api_address_retrieve'),
    re_path('^api/(?P<version>(v1|v2))/address/update/(?P<id>\d+)$', api.AddressUpdate.as_view(), name='api_address_update'),
    re_path('^api/(?P<version>(v1|v2))/address/delete/(?P<id>\d+)$', api.AddressDelete.as_view(), name='api_address_delete'),
        # re_path('^api/(?P<version>(v1|v2))/login/list/', api.LoginList.as_view(), name='api_login_list'),
        # re_path('^api/(?P<version>(v1|v2))/login/create/', api.LoginCreate.as_view(), name='api_login_create'),
    re_path('^api/(?P<version>(v1|v2))/user/login/', api.LoginAPIView.as_view(), name='api_user_login'),
]