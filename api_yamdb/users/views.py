import secrets
from rest_framework import viewsets, permissions, status, mixins
from django.core.mail import send_mail
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .models import User
from .permissions import IsAdmin
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    TokenReceiveSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin, )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ('get', 'post', 'patch', 'delete', )

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            data = request.data.dict()
            if 'role' in data:
                data.pop('role')
            serializer = UserSerializer(
                request.user,
                data=data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenReceiveViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = TokenReceiveSerializer

    def create(self, request):
        serializer = TokenReceiveSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = get_object_or_404(User, username=username)
            if user.confirmation_code == confirmation_code:
                data = {'token': str(AccessToken.for_user(user))}
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                "wrong confirmation code",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserRegistrationViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user, _ = User.objects.get_or_create(**serializer.validated_data)
            confirmation_code = secrets.token_hex(4)
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                subject='Код подтверждения.',
                message=f'Код подтверждения: {confirmation_code}',
                from_email='yamdb@support.com',
                recipient_list=(user.email,),
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
