from rest_framework import serializers
from rest_framework.authtoken.models import Token

from auth_server.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "nickname",
            "first_name",
            "last_name",
            "patronymic",
            "phone",
            "sex",
            "password",
            "token"
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token, created = Token.objects.get_or_create(user=user)
        user.token = token
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "avatar",
            "banner_image",
            "about_me",
            "nickname",
            "id"
        )