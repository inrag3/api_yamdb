from django.urls import path, include
from users.views import TokenReceiveViewSet, UserRegistrationViewSet
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path(
        'v1/auth/token/',
        TokenReceiveViewSet.as_view({'post': 'create'}),
    ),
    path(
        'v1/auth/signup/',
        UserRegistrationViewSet.as_view({'post': 'create'}),
    ),
    path('v1/', include(router.urls)),
]
