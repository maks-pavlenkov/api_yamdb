from django.shortcuts import get_object_or_404
from reviews.models import Genre, Category, Title
from rest_framework import viewsets

from .permissions import IsAdminOrReadOnly
from .serializers import (GenreSerializer, CategorySerializer, TitleSerializer)


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