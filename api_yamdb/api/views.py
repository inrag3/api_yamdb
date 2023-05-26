from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Genre, Category
from .serializers import (TitleSerializer,
                          TitleSlugSerializer,
                          GenreSerializer,
                          CategorySerializer)
from .mixins import CreateListRetrieveViewSet, TitleCreateMixin


class TitleViewSet(TitleCreateMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug', 'category__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ['partial_update', 'create']:
            return TitleSlugSerializer
        return TitleSerializer


class GenreViewSet(CreateListRetrieveViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateListRetrieveViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
