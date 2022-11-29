from django.conf import settings
from reviews import validators
from datetime import date

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Genre, GenreTitle, Title

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с объектами класса User."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')

    def validate_username(self, value):
        """Проверяет, что username состоит из разрешенных символов."""
        validators.validate_username(value)
        return value


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя."""

    username = serializers.CharField(max_length=settings.MAX_NAME_LENGTH)
    email = serializers.EmailField(max_length=settings.MAX_EMAIL_LENGTH)


class TokenSerializer(serializers.Serializer):
    """Сериализатор для обмена кода подтверждения на токен."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleGetSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data)
        print(genres)
        for genre in genres:
            genre_obj = get_object_or_404(Genre, slug=genre['slug'])
            GenreTitle.objects.create(genre=genre_obj, title=title)
        category_obj = get_object_or_404(Category, slug=category['slug'])
        title = Title.objects.create(
            genre=GenreTitle.genre,
            category=category_obj,
            **validated_data
        )
        return title


class TitlePostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate(self, data):
        title_year = data['year']
        current_year = date.today().year
        if title_year > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)
