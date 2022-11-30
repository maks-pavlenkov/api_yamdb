from datetime import date

from django.conf import settings
from rest_framework import serializers
from reviews import validators
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

    def validate_username(self, value):
        """Проверяет, что username состоит из разрешенных символов."""
        validators.validate_username(value)
        return value


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
    rating = serializers.IntegerField(read_only=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', many=True,
                                         queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        # fields = '__all__'

    def validate(self, data):
        if 'year' in data:
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

    def create(self, validated_data):
        title = validated_data.get('title')
        author = validated_data.get('author')
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                'You cannot add more than one review'
            )
        return Review.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)
