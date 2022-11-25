from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    USER = "Пользователь"
    MODERATOR = "Модератор"
    ADMIN = "Администратор"
    ROLES = [
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор")
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=254,
        unique=True)
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True)
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True)
    bio = models.TextField(
        blank=True,
        null=True)
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default=USER
    )

