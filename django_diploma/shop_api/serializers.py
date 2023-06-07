from rest_framework import serializers

from .models import Avatar, Profile


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['src', 'alt']


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(required=False)

    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'avatar']
