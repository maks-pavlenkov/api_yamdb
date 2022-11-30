from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_username

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

ROLES = [
    (USER, "Пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор")
]


class User(AbstractUser):
    """Кастомизированная модель пользователя."""

    username = models.CharField(
        max_length=settings.MAX_NAME_LENGTH,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True)
    first_name = models.CharField(
        max_length=settings.MAX_NAME_LENGTH,
        blank=True,
        null=True)
    last_name = models.CharField(
        max_length=settings.MAX_NAME_LENGTH,
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
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=settings.MAX_NAME_LENGTH)
    slug = models.SlugField(unique=True) # без этого падает один тест

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

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(settings.MIN_RATING_VALUE),
            MaxValueValidator(settings.MAX_RATING_VALUE)
        ]
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(max_length=500)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
