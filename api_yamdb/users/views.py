from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .permissions import (IsAdminOrSuperuser)
from .serializers import (SignUpSerializer, TokenSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели User.
    Используется только аутентифицированными пользователями с правами админов
    (кроме доступа к users/me, который доступен любому аутентифицированному
    пользователю).
    """
    permission_classes = (IsAdminOrSuperuser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,))
    def me(self, request):
        """
        Возвращает аутентифицированному пользователю данные его учетной записи
        (GET-запрос) и позволяет их изменить (PATCH-запрос).
        """
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data)


class SignUpView(APIView):
    """
    Вью-класс для регистрации и получения confirmation code.
    Разрешается только POST-запрос. Доступ без токена.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Используя переданные пользователем username и email,
        создает нового пользователя, если его еще нет в базе,
        и отправляет на указанный email код подтверждения.
        """
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user = User.objects.get(username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Your confirmation code',
            message=f'Your code: {confirmation_code}. Use it wisely.',
            from_email='signup@yamdb.com',
            recipient_list=(email,))
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK)


class TokenView(APIView):
    """
    Вью-класс для обмена confirmation code на JWT Access Token.
    Разрешается только POST-запрос. Доступ без токена.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Проверяет переданный пользователем confirmation_code
        и возвращает JWT токен.
        """
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)

        return Response(
            {'confirmation_code': ['Invalid confirmation code!']},
            status=status.HTTP_400_BAD_REQUEST)
