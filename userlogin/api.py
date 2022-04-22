from django.contrib.auth.models import update_last_login
from django.http import Http404
from rest_framework import generics, status, versioning
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from userlogin.models import MyUser, Address
from userlogin.serializer import UserSerializer, UserSerializerV1, AddressSerializerV1, AddressSerializer, \
    LoginSerializer
from rest_framework.versioning import URLPathVersioning


class CustomNumberPagination(PageNumberPagination):
    page_size = 10  # Put the number of items you want in one page


# class ExampleVersioning(URLPathVersioning):
#     allowed_versions = ('v1', 'v2', )


class UserList(APIView):
    """List all Users, and Create New user."""
    versioning_class = URLPathVersioning
    users = MyUser.objects.all()
    # serializer_class = UserSerializer

    def get(self, request, version=versioning_class, users=users):
        if version == 'v2':
            serializer = UserSerializerV1(users, many=True)
            return Response(serializer.data)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, version=versioning_class):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """Retrieve, update and delete user."""
    versioning_class = URLPathVersioning

    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, version=versioning_class):
        user = self.get_object(pk)
        if version == 'v2':
            serializer = UserSerializerV1(user)
            return Response(serializer.data)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, version=versioning_class):
        user = self.get_object(pk)
        if version == 'v2':
            serializer = UserSerializerV1(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, version=versioning_class):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAPIView(APIView):
        authentication_classes = (TokenAuthentication,)
        permission_classes = (AllowAny,)

        def get(self, request, *args, **kwargs):
            user = MyUser.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        # serializer = LoginSerializer(data=request.data, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['username']
        # update_last_login(None, user)
        # token, created = Token.objects.get_or_create(username=user)
        # return Response({"status": status.HTTP_200_OK, "Token": token.key})

# class UserList(generics.ListAPIView):
#     """API for the user using LIStAPIView for view and edit user"""
#     versioning_class = URLPathVersioning
#     queryset = MyUser.objects.all()
#     serializer_class = UserSerializer
#
#     def get_serializer_class(self):
#         """
#         get version and called serializer according version.
#         """
#         if self.request.version == 'v2':
#             return UserSerializerV1
#         return UserSerializer
#
#
# class UserCreate(generics.ListCreateAPIView):
#     """API for the user registration using ListCreateAPIView"""
#     versioning_class = URLPathVersioning
#     queryset = MyUser.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserRetrieve(generics.RetrieveAPIView):
#     """API for the retrieve user using RetrieveAPIView"""
#     versioning_class = URLPathVersioning
#     queryset = MyUser.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = "id"
#
#
# class UserUpdate(generics.UpdateAPIView):
#     """API for the user update using UpdateAPIView"""
#     versioning_class = URLPathVersioning
#     queryset = MyUser.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = "id"
#
#
# class UserDelete(generics.RetrieveDestroyAPIView):
#     """API for the delete user using RetrieveDestroyAPIView"""
#     versioning_class = URLPathVersioning
#     queryset = MyUser.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = "id"


class AddressList(generics.ListAPIView):
    """API for the Address using LIStAPIView for view and edit address"""
    versioning_class = URLPathVersioning
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_serializer_class(self):
        """
        get version and called serializer according version.
        """
        if self.request.version == 'v2':
            return AddressSerializerV1
        return AddressSerializer


class AddressCreate(generics.ListCreateAPIView):
    """API for the new address using ListCreateAPIView"""
    versioning_class = URLPathVersioning
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressRetrieve(generics.RetrieveAPIView):
    """API for the retrieve address using RetrieveAPIView"""
    versioning_class = URLPathVersioning
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = "id"


class AddressUpdate(generics.UpdateAPIView):
    """API for the address update using UpdateAPIView"""
    versioning_class = URLPathVersioning
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = "id"


class AddressDelete(generics.RetrieveDestroyAPIView):
    """API for to delete address using RetrieveDestroyAPIView"""
    versioning_class = URLPathVersioning
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = "id"