import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import Profile


def get_data(request: Request) -> dict:
    print(request.data)
    return json.loads(next(iter(request.data)))


class SignIn(APIView):
    def post(self, request: Request) -> Response:
        auth_data = get_data(request)
        username = auth_data.get('username')
        password = auth_data.get('password')
        user = authenticate(
            self.request,
            username=username,
            password=password,)
        if user:
            login(request=self.request, user=user)
            return Response(status=200)
        else:
            return Response(status=401)


class SignUp(APIView):
    def post(self, request: Request) -> Response:
        register_data = get_data(request)
        username = register_data.get('username')
        password = make_password(register_data.get('password'))
        print(register_data)
        try:
            user = User.objects.get(username=username)
            if user.password != password:
                return Response(status=401)
        except User.DoesNotExist:
            user = User.objects.create(
                username=username,
                password=password,
            )
            Profile.objects.create(user=user)


        login(request=self.request, user=user)

        return Response(status=200)
