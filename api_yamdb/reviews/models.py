from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title', null=True
    )
    year = models.PositiveIntegerField(db_index=True)
    genre = models.ManyToManyField(
        Genre, related_name='title',
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

    class Meta:
        unique_together = ('author', 'title')
        ordering = ('pub_date',)

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

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('genre', 'title',)

    def __str__(self):
        return f'{self.genre} {self.title}'
