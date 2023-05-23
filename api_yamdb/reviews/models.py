from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    category = models.ForeignKey(Category, related_name='titles', on_delete=models.SET_NULL, blank=False, null=True)
    genre = models.ManyToManyField(Genre, related_name='titles', blank=False, null=True)
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    rating = models.FloatField()


class TitleGroup(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
