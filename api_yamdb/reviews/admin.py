from django.contrib import admin

from .models import Title, Genre, Category, TitleGenre


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'slug',
                    'name',
                    )
    search_fields = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'slug',
                    'name',
                    )
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'year',
                    'category_name',
                    'display_genres',
                    'description',
                    )
    search_fields = ('name', 'year', )
    empty_value_display = '-пусто-'
    list_editable = ('name', 'year')

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    def category_name(self, obj):
        return obj.category.name


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'title_name',
                    'genre_name',
                    )
    search_fields = ('title_name', 'genre_name')

    def genre_name(self, obj):
        return obj.genre.name

    def title_name(self, obj):
        return obj.title.name

admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)
