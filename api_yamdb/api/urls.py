from rest_framework import routers

from django.urls import include, path

from .views import GenreViewSet, CategoryViewSet, TitleViewSet, ReviewsViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
urlpatterns = [
    path('v1/', include(router.urls))
]
