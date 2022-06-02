# userlogin.authentication

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class SafeJWTAuthentication(BaseAuthentication):
    '''custom authentication class for authenticate token.'''

    def authenticate(self, request):
        # import pdb; pdb.set_trace()
        User = get_user_model()
        print(':::::::',User)
        authorization_heaader = request.headers.get('Authorization')  # get the bearer token.

        if not authorization_heaader:
            return None
        try:
            access_token = authorization_heaader.split(' ')[1]  # get the token only.
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired, Please enter valid access token.')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(id=payload['user_id']).first()
        print('"""""""', payload["user_id"], user)
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        return (user, None)