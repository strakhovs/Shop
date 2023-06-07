import io
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import Profile, Avatar, profile_avatar_directory_path
from .serializers import AuthSerializer, RegisterSerializer, ProfileSerializer, AvatarSerializer


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
            profile = Profile.objects.create(user=user)
            Avatar.objects.create(profile_id=profile.pk)
        login(request=self.request, user=user)
        return Response(status=200)


class ProfileView(APIView):
    def get(self, request: Request) -> Response:
        profile = Profile.objects.get(user_id=request.user)
        print(profile)
        serializer = ProfileSerializer(profile)

        data = JSONRenderer().render(serializer.data)
        print(serializer.data)
        print(data)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        print(request.data)
        profile = Profile.objects.get(user_id=request.user)
        data = request.data
        serializer = ProfileSerializer(data=data)
        serializer.is_valid()
        profile.fullName = serializer.validated_data.get('fullName')
        profile.email = serializer.validated_data.get('email')
        profile.phone = serializer.validated_data.get('phone')
        profile.save()
        serializer = ProfileSerializer(profile)
        data = JSONRenderer().render(serializer.data)
        return Response(data)


class AvatarUpdateView(APIView):
    def post(self, request: Request) -> Response:
        print(request.FILES)
        profile = Profile.objects.get(user=request.user)
        avatar = Avatar.objects.get(profile_id=profile.pk)
        avatar.avatar = request.FILES["avatar"]
        filename = request.FILES["avatar"].name
        avatar.src = '/media/' + profile_avatar_directory_path(profile, filename)
        print(avatar.src, '!!!!!!!!!!!!!!!!!!!!!!')
        avatar.alt = 'avatar'
        avatar.save()
        serializer = AvatarSerializer(avatar)
        print(serializer.data)
        data = JSONRenderer().render(serializer.data)
        print(data)
        return Response(data)


class PasswordUpdateView(APIView):
    def post(self, request: Request) -> Response:
        user = request.user
        print(request.data)
        return Response(status=200)
