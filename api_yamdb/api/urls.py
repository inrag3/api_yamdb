from django.urls import path
from users.views import TokenReceiveViewSet, UserRegistrationViewSet


urlpatterns = [
    path('v1/auth/token/', TokenReceiveViewSet.as_view()),
    path('v1/auth/signup/', UserRegistrationViewSet.as_view()),
]
