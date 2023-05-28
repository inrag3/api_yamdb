from rest_framework import serializers
from .models import User


class UserSerializer(serializers.BaseSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserRegistrationSerializer(serializers.BaseSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenReceiveSerializer(serializers.BaseSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True,
    )
