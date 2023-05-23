from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

# class Review(models.Model):
#     text = models.TextField()
#     score = models.IntegerField()
#     title = models.ForeignKey(Title, related_name='reviews' )


class Title(models.Model):
    category = models.ForeignKey(Category, related_name='titles', blank=False, null=True, on_delete=models.SET_NULL)
    genre = models.ManyToManyField(Genre, related_name='titles', blank=False)
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    #rating = 


class TitleGroup(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
