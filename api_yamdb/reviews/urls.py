from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet

router = DefaultRouter()

router.register(r'titles', TitleViewSet)

app_name = 'reviews'
urlpatterns = [
    path('', include(router.urls)),
]
