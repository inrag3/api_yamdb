from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Title, Genre, Category

class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                     queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug',
                                  queryset=Genre.objects.all(),
                                  many =True)

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Title
        fields = '__all__'
