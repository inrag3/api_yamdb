from rest_framework import viewsets, mixins
from rest_framework.response import Response

from reviews.models import Genre, Category
from .serializers import (GenreSerializer,
                          CategorySerializer)


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return self.change_data(response)
