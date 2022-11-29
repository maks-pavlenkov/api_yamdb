from django.conf import settings
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


class Category(models.Model):
    name = models.CharField(max_length=settings.MAX_NAME_LENGTH)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=settings.MAX_NAME_LENGTH)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=settings.MAX_NAME_LENGTH)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="title", null=True
    )
    year = models.IntegerField()
    genre = models.ManyToManyField(
        Genre, related_name="title",
        through='GenreTitle',
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
