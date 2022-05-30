import re

from django.http import Http404
from rest_framework import generics, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from userlogin import methods
from userlogin.models import MyUser, Address
from userlogin.serializer import UserSerializer, UserSerializerV1, AddressSerializerV1, AddressSerializer \
    , EmailVerificationSerializer
from userlogin.views import userlogin_info_logger, userlogin_debug_logger, userlogin_warning_logger

EMAIL_REQUIRED = 'email must be required here!!'
PASSWORD_CHANGE_SUCCESS_MSG = 'Password updated Successfully!!Please login into System with your new password..'
CODE_NOT_VALID_MSG = 'Oops!!code is not valid..Please try again..'
SERIALIZER_NOT_VALID_MSG = 'Serializer is not valid'
USER_NOT_EXISTS = 'User not exists.!!'
EMAIL_VALID_MSG = 'Please enter valid email'
USERLOGIN_V2_LOG_MSG = "User serializer v2 called with username field only."
USERLOGIN_V1_LOG_MSG = "User serializer v1 called with all the fields."
USER_CREATED_LOG_MSG = 'User created successfully.'
USER_CREATED_ERROR = 'User not created successfully please fill valid details.'
USER_RETRIEVE_LOG_MSG = 'User Retrieve successfully.'
USER_NOT_EXISTS_LOG_MSG = 'User not exists.'
GET_USER_LOG_MSG = 'user get successfully.'
USER_UPDATE_LOG_MSG = 'user updated successfully.'
USER_UPDATE_ERROR_LOG_MSG = 'please fill in valid user details.'
USER_DELETE_LOG_MSG = 'User deleted successfully.'
CURRENT_LOGIN_USER_LIST_LOAD_LOG_MSG = 'Currently logged in user list display successfully.'
ADDRESS_LIST_LOAD_LOG_MSG = 'Address list load successfully.'
ADDRESS_CREATED_LOG_MSG = 'Address created successfully.'
ADDRESS_RETRIEVE_LOG_MSG = 'Address retrieved successfully.'
ADDRESS_UPDATE_LOG_MSG = 'Address Updated Successfully.'
ADDRESS_DELETED_LOG_MSG = 'Address Deleted Successfully.'
TOKEN_CREATED_LOG_MSG = 'Token created Successfully.'


class CustomNumberPagination(PageNumberPagination):
    """pagination class."""
    page_size = 10  # Put the number of items you want in one page


class UserList(APIView):
    """List all Users, and Create New user."""
    versioning_class = URLPathVersioning  # version type for the versioning
    users = MyUser.objects.all()  # fetch all the users.

    lookup_field_kwargs = ['id', ]

    def get(self, request, version=versioning_class, users=users):
        """get list of users."""
        if version == 'v2':  # check version
            serializer = UserSerializerV1(users, many=True)  # call serializer according version
            userlogin_info_logger.info(USERLOGIN_V2_LOG_MSG)
            return Response(serializer.data)  # return response
        serializer = UserSerializer(users, many=True, context={'request': request})  # call serializer according version
        userlogin_info_logger.info(USERLOGIN_V1_LOG_MSG)
        return Response(serializer.data)

    def post(self, request, version=versioning_class):
        """create new user."""
        serializer = UserSerializer(data=request.data, context={'request': request})  # call serializer
        if serializer.is_valid():  # check that serializer is valid or not
            serializer.save()
            userlogin_debug_logger.debug(USER_CREATED_LOG_MSG)
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # created successfully
        userlogin_warning_logger.warning(USER_CREATED_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # bad request


class UserDetail(APIView):
    """Retrieve, update and delete user."""
    versioning_class = URLPathVersioning  # declare version type which version we will use.

    def get_object(self, pk):
        """get object and if not exists then rais exception."""
        try:
            userlogin_info_logger.info(USER_RETRIEVE_LOG_MSG)
            return MyUser.objects.get(pk=pk)  # get object according pk.
        except MyUser.DoesNotExist:  # not exists then rais exception
            userlogin_warning_logger.warning(USER_NOT_EXISTS_LOG_MSG)
            raise Http404

    def get(self, request, pk, version=versioning_class):
        """get users list."""
        user = self.get_object(pk)  # call get object method
        serializer = UserSerializerV1(user) if version == 'v2' else UserSerializer(user, context={'request': request})  # check version and call
        # serializer accordingly.
        userlogin_info_logger.info(GET_USER_LOG_MSG)
        return Response(serializer.data)

    def put(self, request, pk, version=versioning_class):
        """update users according."""
        user = self.get_object(pk)  # call get object method
        serializer = UserSerializerV1(user, data=request.data) if version == 'v2' else UserSerializer(user, data=request.data, context={'request': request})  # check version and call serializer accordingly
        if serializer.is_valid():  # check serializer is valid or not
            serializer.save()
            userlogin_info_logger.info(USER_UPDATE_LOG_MSG)
            return Response(serializer.data)
        userlogin_warning_logger.warning(USER_UPDATE_ERROR_LOG_MSG)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, version=versioning_class):
        """delete user according pk."""
        user = self.get_object(pk)  # call get object method
        user.delete()  # delete record.
        userlogin_info_logger.info(USER_DELETE_LOG_MSG)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAPIView(viewsets.ModelViewSet):
    """API for the user Login"""
    # permission_classes = (IsAuthenticated,)  # check permission
    serializer_class = UserSerializer  # set serializer class.

    def get_queryset(self):
        """display list of only currently logged-in user."""
        userlogin_info_logger.info(CURRENT_LOGIN_USER_LIST_LOAD_LOG_MSG)
        return MyUser.objects.filter(username=self.request.user)


class AddressList(generics.ListAPIView):
    """API for the Address using LIStAPIView for view and edit address"""
    userlogin_info_logger.info(ADDRESS_LIST_LOAD_LOG_MSG)
    versioning_class = URLPathVersioning  # set versioning class which version we will use.
    queryset = Address.objects.all()  # fetch all the records.
    serializer_class = AddressSerializer  # set serializer class.
    permission_classes = [IsAuthenticated]  # user need to log in into system to access this api.

    def get_serializer_class(self):
        """
        get version and called serializer according version.
        """
        return AddressSerializerV1 if self.request.version == 'v2' else AddressSerializer  # check version and call
        # serializer accordingly.


class AddressCreate(generics.ListCreateAPIView):
    """API for the new address using ListCreateAPIView"""
    userlogin_info_logger.info(ADDRESS_CREATED_LOG_MSG)
    versioning_class = URLPathVersioning  # set versioning class, which version type we will use.
    queryset = Address.objects.all()  # fetch all the users.
    serializer_class = AddressSerializer  # set serializer class
    permission_classes = [IsAuthenticated]  # user need to log in into system to access this api.

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response({"status": True,
    #                      "message": "Organization Added !",
    #                      "data": serializer.data},
    #                     status=status.HTTP_201_CREATED, headers=headers)

class AddressRetrieve(generics.RetrieveAPIView):
    """API for the retrieve address using RetrieveAPIView"""
    userlogin_info_logger.info(ADDRESS_RETRIEVE_LOG_MSG)
    versioning_class = URLPathVersioning  # set versioning class, which we will use.
    queryset = Address.objects.all()  # fetch all the users.
    serializer_class = AddressSerializer  # set serializer class
    lookup_field = "id"  # set unique field as lookup_field.
    permission_classes = [IsAuthenticated]  # user need to log in into system to access this api.


class AddressUpdate(generics.UpdateAPIView):
    """API for the address update using UpdateAPIView"""
    userlogin_info_logger.info(ADDRESS_UPDATE_LOG_MSG)
    versioning_class = URLPathVersioning  # set versioning class, which we will use.
    queryset = Address.objects.all()  # fetch all the users.
    serializer_class = AddressSerializer  # set serializer class
    lookup_field = "id"  # set unique field as lookup_field.
    permission_classes = [IsAuthenticated]  # user need to log in into system to access this api.


class AddressDelete(generics.RetrieveDestroyAPIView):
    """API for to delete address using RetrieveDestroyAPIView"""
    userlogin_info_logger.info(ADDRESS_DELETED_LOG_MSG)
    versioning_class = URLPathVersioning  # set versioning class, which we will use.
    queryset = Address.objects.all()  # fetch all the users.
    serializer_class = AddressSerializer  # set serializer class
    lookup_field = "id"  # set unique field as lookup_field.
    permission_classes = [IsAuthenticated]  # user need to log in into system to access this api.


class EmailVerify(APIView):
    """API for email verification and code generate"""
    versioning_class = URLPathVersioning  # set versioning class, which we will use.

    def post(self, request, format=None, version=versioning_class):
        """verify email and generate token for that user."""
        email = request.POST.get('email')
        if email:
            if re.match("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", str(email), re.IGNORECASE):
                instance = MyUser.objects.filter(email=email).first()
                if not instance:  # check that user exists
                    userlogin_info_logger.info(USER_NOT_EXISTS_LOG_MSG)
                    return Response({'message': USER_NOT_EXISTS})
                code = methods.send_verification_mail(email)
                instance.code = code[0]  # fetch code and change accordingly in user record.
                instance.save()
                userlogin_info_logger.info(TOKEN_CREATED_LOG_MSG)
                return Response(request.data, status=status.HTTP_201_CREATED)  # if successfully created.
            userlogin_info_logger.info(EMAIL_VALID_MSG)
            return Response({'message': EMAIL_VALID_MSG})
        userlogin_warning_logger.warning(EMAIL_REQUIRED)
        return Response({'message': EMAIL_REQUIRED})


class CodeView(APIView):
    """API for code and email verify"""
    versioning_class = URLPathVersioning  # set versioning class, which we will use.

    def post(self, request, format=None, version=versioning_class):
        """fetch user according email and then verify generate code and set new password accordingly."""
        serializer = EmailVerificationSerializer(data=request.data)  # call serializer

        if serializer.is_valid():  # check that serializer is valid or not
            USER = MyUser.objects.filter(code=serializer.validated_data['code'],
                                         email=serializer.validated_data['email'])
            if USER.exists():  # check that user is exists
                # with this code and email address.
                user = USER.first()  # filter data according code.
                user.code = 1  # update code as 1.
                user.set_password(serializer.validated_data['newPassword'])  # change password.
                user.save()
                userlogin_info_logger.info(PASSWORD_CHANGE_SUCCESS_MSG)
                return Response({'message': PASSWORD_CHANGE_SUCCESS_MSG})  # return message if code and email is equal
            else:
                userlogin_debug_logger.debug(CODE_NOT_VALID_MSG)
                return Response({'message': CODE_NOT_VALID_MSG})  # return message if email and code is not equal.
        else:
            userlogin_debug_logger.debug(SERIALIZER_NOT_VALID_MSG)
            return Response({'message': SERIALIZER_NOT_VALID_MSG})  # return message is serializer is not valid.


# class TokenObtainPairView(TokenViewBase):
#     print("token obtains from here.")
#     print("token obtains from here.")
#     pass