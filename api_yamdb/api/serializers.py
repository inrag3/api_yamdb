from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Title,
    Genre,
    Category,
    Comment,
    Review,
)

from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    ValidationError,
)

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = 'name', 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = 'name', 'slug'

        
class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True, )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, year):
        present_year = datetime.now().year
        if year > present_year:
            raise serializers.ValidationError(
                'Год выпуска фильма не может быть больше текущего года!')
        if year < 1895:
            raise serializers.ValidationError('Кино еще не появилось!')
        return year

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(score=Avg('score'))
        return rating.get('score')


class TitleSlugSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genre.objects.all())
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise ValidationError(
                'Это ошибка, вызванная тем, что нельзя оставлять'
                'два отзыва на одно произведение'
            )
        return data

class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
