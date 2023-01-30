from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Кастомизированная модель пользователя."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    MAX_NAME_LENGTH = 150
    MAX_EMAIL_LENGTH = 254
    ROLES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]

    username = models.CharField(
        max_length=MAX_NAME_LENGTH,
        unique=True,
        validators=[validate_username])
    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True)
    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        blank=True,
        null=True)
    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
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

    @property
    def is_admin_or_superuser(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
