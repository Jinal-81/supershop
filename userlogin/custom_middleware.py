from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class DemoMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)  # get response.
        if response.status_code == 403:  # check response status is 403 then give custom message.
            return JsonResponse("Error:access_token expired, Please enter valid access token.", safe=False)
        else:  # else return same response data.
            return response