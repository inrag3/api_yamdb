from rest_framework.response import Response
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Genre, Category
from .serializers import TitleSerializer, TitleSlugSerializer, GenreSerializer, CategorySerializer


class TitleCreateMixin(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin):
    def change_data(self, response):
        category_object = Category.objects.get(slug=response.data['category'])
        serialised_category = CategorySerializer(category_object)
        response.data['category'] = serialised_category.data
        genres = response.data['genre']
        response.data['genre'] = []
        for slug in genres:
            genre_object = Genre.objects.get(slug=slug)
            serialised_genre = GenreSerializer(genre_object)
            response.data['genre'].append(serialised_genre.data)
        return response

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', None)
        if partial is None:
            return Response({
                                "detail": "Method \"PUT\" not allowed."
                            }, '405')
        response = super().update(request, *args, **kwargs)
        return self.change_data(response)
    
    def create (self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.change_data(response)


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


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'