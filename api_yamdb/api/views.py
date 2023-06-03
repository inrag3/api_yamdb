from rest_framework import viewsets, mixins, filters, permissions, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.decorators import action
from api_yamdb.settings import EMAIL
from reviews.models import Title, Genre, Category, Review, Title
from .permissions import (
    IsAdmin,
    IsAdminOrModeratorOrOwnerOrReadOnly,
    IsAdminOrReadOnly,
)
from .serializers import (
    TitleWriteSerializer,
    TitleReadSerializer,
    GenreSerializer,
    CategorySerializer,
    CommentSerializer,
    ReviewSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    TokenReceiveSerializer,
)
from .mixins import CreateDestroyListViewSet

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year')
    http_method_names = ('get', 'post', 'patch', 'delete', )

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleWriteSerializer
        return TitleReadSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        genre_slug = self.request.query_params.get('genre')
        category__slug = self.request.query_params.get('category')
        if genre_slug is not None:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category__slug is not None:
            queryset = queryset.filter(category__slug=category__slug)
        return queryset


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminOrModeratorOrOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrModeratorOrOwnerOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        return review.comments.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin, )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ('get', 'post', 'patch', 'delete', )

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            data = request.data.dict()
            if 'role' in data:
                data.pop('role')
            serializer = UserSerializer(
                request.user,
                data=data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenReceiveViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = TokenReceiveSerializer

    def create(self, request):
        serializer = TokenReceiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            data = {'token': str(AccessToken.for_user(user))}
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            "wrong confirmation code",
            status=status.HTTP_400_BAD_REQUEST
        )


class UserRegistrationViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        print(confirmation_code)
        send_mail(
            subject='Код подтверждения.',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=EMAIL,
            recipient_list=(user.email,),
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
