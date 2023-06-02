from django.contrib.auth.models import AbstractUser
from django.db import models
from api_yamdb.settings import ROLES, USER, ADMIN, MODERATOR
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$'
            )
        ],
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=ROLES,
        default=USER,
        max_length=10,
    )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    def __str__(self) -> str:
        return f'{self.username}'
