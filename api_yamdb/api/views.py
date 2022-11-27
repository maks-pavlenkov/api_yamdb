from django.shortcuts import get_object_or_404
from reviews.models import Genre, Category, Title
from rest_framework import viewsets
from rest_framework import filters

from .permissions import IsAdminOrReadOnly
from .serializers import (
    GenreSerializer, CategorySerializer, TitleSerializer, ReviewsSerializer
)
from reviews.models import Genre, Category, Title


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        return get_object_or_404(Title, pk=self.kwargs.get('titles_id'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ('pub_date',)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author='Test', title=self.get_title())
