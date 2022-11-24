from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = "Пользователь"
    MODERATOR = "Модератор"
    ADMIN = "Администратор"
    ROLES = [
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор")
    ]
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default=USER
    )
