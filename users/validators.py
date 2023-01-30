import re

from django.core.exceptions import ValidationError


def validate_username(username):
    """Проверяет корректность поля username."""

    PATTERN = re.compile(r'^[\w.@+-]+\Z')

    if username.lower() == 'me':
        raise ValidationError(
            message='Использовать имя "me" в качестве username запрещено. '
        )
    if not PATTERN.findall(username):
        raise ValidationError(
            'Username содержит некорректные символы.'
        )
