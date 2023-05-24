from rest_framework.response import Response
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Genre, Category
from .serializers import TitleSerializer, TitleSlugSerializer, GenreSerializer, CategorySerializer


class TitleCreateMixin(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin):
    pass
    def update(self, request, *args, **kwargs):
        wtf = super().update(request, *args, **kwargs)
        print(f"XXX {wtf} XXX")
        return wtf
        # partial = kwargs.pop('partial', False)
        # if partial == False:
        #     return Response        #    здесь выдать такой ответ {"detail": "Method \"PUT\" not allowed."} со статус кодом 405
        # instance = self.get_object()      #  и дальше как
        # serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)


class TitleViewSet(TitleCreateMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug', 'category__slug', 'name', 'year')

    def get_serializer_class(self):
        print(self.action)
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