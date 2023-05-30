from django.contrib import admin

from reviews.models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    search_fields = ('title', 'author', 'text')
    list_filter = ('pub_date', 'score', 'author')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
