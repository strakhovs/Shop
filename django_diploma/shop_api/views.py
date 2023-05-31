import io
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import Profile
from .serializers import AuthSerializer, RegisterSerializer


class SignIn(APIView):
    def post(self, request: Request) -> Response:
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = AuthSerializer(data=data)
        serializer.is_valid()
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
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
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = RegisterSerializer(data=data)
        serializer.is_valid()
        name = serializer.validated_data.get('name')
        username = serializer.validated_data.get('username')
        password = make_password(serializer.validated_data.get('password'))
        try:
            User.objects.get(username=username)
            return Response(status=401)
        except User.DoesNotExist:
            user = User.objects.create(
                first_name=name,
                username=username,
                password=password,
            )
            Profile.objects.create(user=user)
        login(request=self.request, user=user)
        return Response(status=200)
