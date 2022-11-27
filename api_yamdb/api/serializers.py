from django.conf import settings

from rest_framework import serializers

from reviews.models import User
from reviews import validators


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