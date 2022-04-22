from rest_framework import serializers
from userlogin.models import MyUser, Address


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user."""
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile_number', 'profile_pic', ]


class UserSerializerV1(serializers.ModelSerializer):
    """serializer for the username only using versioning."""
    class Meta:
        model = MyUser
        fields = ['username', ]


class LoginSerializer(serializers.ModelSerializer):
    """serializer for user login."""
    class Meta:
        model = MyUser
        fields = ['username', 'password', ]


class AddressSerializer(serializers.ModelSerializer):
    """serializer for address."""
    class Meta:
        model = Address
        fields = '__all__'


class AddressSerializerV1(serializers.ModelSerializer):
    """serializer for the city only using versioning."""
    class Meta:
        model = Address
        fields = ['city', ]


