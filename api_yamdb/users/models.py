from django.contrib.auth.models import AbstractUser
from django.db import models
from api_yamdb.settings import ROLES, USER, ADMIN, MODERATOR
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$'
            )
        ]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    role = models.CharField(
        choices=ROLES,
        default=USER,
        max_length=10,
    )
    confirmation_code = models.CharField(
        max_length=32,
    )

    def is_user(self):
        return self.role == USER

    def is_moderator(self):
        return self.role == MODERATOR

    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    def __str__(self) -> str:
        return f'{self.username}'
