from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import detail_route, list_route
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import datetime, now, timedelta, utc


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    @list_route(methods=['post'], url_path='register')
    def user_register(self, request):
        """
        Registered user
        :param request
        :return: response
        """
        userS = UserSerializer(data=request.data)

        if userS.is_valid():
            user = userS.save()     # add to db
            password = user.password
            user.set_password(password)     # encrypt the password
            user.save()
            return Response(userS.data, status=202)
        else:
            return Response(userS.errors, status=400)

    @list_route(methods=['post'], url_path='login')
    def user_login(self, request):
        """
        log in the user
        :param request:
        :return: response & valid token
        """
        try:
            username = request.data['username']
            password = request.data['password']
        except MultiValueDictKeyError:
            return Response({"message": "No user Information"}, status=404)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user=user)
                token_request = {"token": token.key}
            except Token.DoesNotExist:
                raise AuthenticationFailed('Invalid token')
            return Response(token_request, status=200)
        else:
            return Response({"message": "Invalid Login Information"}, status=400)


    @list_route(methods=['post'], url_path='auth')
    def authenticate_token(self, request):
        try:
            token = Token.objects.get(key=request.POST['token'])
        except Token.DoesNotExist:
            return Response({"message": "Invalid token"}, status=400)

        if not token.user.is_active:
            return Response({"message": "User inactive"}, status=404)

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=utc)

        if token.created < utc_now - timedelta(days=7):
            return Response({"message": "Token expired"}, status=402)

        return Response({"message": "success"}, status=200)
