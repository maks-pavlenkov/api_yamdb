from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, SignUpView, TokenView

app_name = 'users'

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
