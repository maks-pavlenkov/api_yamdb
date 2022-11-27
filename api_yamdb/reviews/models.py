from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="title", blank=False, null=True
    )
    year = models.IntegerField()
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name="title", blank=False, null=True
    )

    def __str__(self):
        return self.name


class Reviews(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=20) # Will fix it later
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
