from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from . import validators
from .models import User


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
    username = serializers.CharField(max_length=User.MAX_NAME_LENGTH)
    email = serializers.EmailField(max_length=User.MAX_EMAIL_LENGTH)

    def validate_username(self, value):
        """Проверяет, что username состоит из разрешенных символов."""
        validators.validate_username(value)
        return value

    def validate(self, data):
        """
        Проверяет, можно ли создавать пользователя с таким username и email.
        """
        try:
            user, is_new = User.objects.get_or_create(
                email=data['email'],
                username=data['username'])
        except IntegrityError:
            raise ValidationError(
                detail=('Невозможно создать пользователя с такими данными: '
                        'username или email уже занят.'
                        )
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для обмена кода подтверждения на токен."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
