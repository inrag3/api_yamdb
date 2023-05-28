from rest_framework import viewsets
from .models import User


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()


class TokenReceiveViewSet(viewsets.ViewSet):
    queryset = User.objects.all()


class UserRegistrationViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

