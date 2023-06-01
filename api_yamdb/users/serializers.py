from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

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


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя \'me\' в качестве username запрещено!'
            )
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'Использовать \'username\' зарегистрированного'
                    ' пользователя и незанятый \'email\' запрещено'
                )
        if User.objects.filter(email=email).exists():
            if not User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    'Использовать \'email\' зарегистрированного пользователя'
                    ' и незанятый \'username\' запрещено'
                )
        return super().validate(data)


class TokenReceiveSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True,
    )
