from rest_framework import routers

from django.urls import include, path

from .views import GenreViewSet, CategoryViewSet, TitleViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='titles')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]