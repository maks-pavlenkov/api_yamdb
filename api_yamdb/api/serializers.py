from django.conf import settings
from reviews import validators
from datetime import date
from rest_framework import serializers

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


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(read_only=True, many=True)
    category = serializers.StringRelatedField(read_only=True)
    description = serializers.StringRelatedField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate(self):
        title_year = int(self.context['year'])
        current_year = date.today().year
        if title_year > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


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
