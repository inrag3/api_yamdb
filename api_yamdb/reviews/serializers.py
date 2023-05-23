from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Title, Genre, Category

class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug',
                                     queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                                  queryset=Genre.objects.all(),
                                  many =True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
    
class TitleListSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug',
                                     queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                                  queryset=Genre.objects.all(),
                                  many =True)

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class GenreSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Category
        fields = '__all__'

