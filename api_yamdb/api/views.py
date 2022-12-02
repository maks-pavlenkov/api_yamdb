from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (AuthorAdminModeratorOrReadOnly, IsAdminOrReadOnly,
                          IsAdminOrSuperuser)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          TokenSerializer, UserSerializer)


class CreateListDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    pass


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
            serializer.save(role=request.user.role)  # пока костыль
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
        try:
            user, is_new = User.objects.get_or_create(
                email=email,
                username=username
            )
        except IntegrityError:
            raise ValidationError(
                detail=('Невозможно создать пользователя с такими данными: '
                        'username или email уже занят.'
                        )
            )
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


class GenreViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class CategoryViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('title', 'pub_date', 'author')
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering = ('review', 'pub_date', 'author')

    def get_review(self):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
