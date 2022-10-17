from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title

# class PostAdmin(admin.ModelAdmin):
# list_display = ('pk', 'text', 'pub_date', 'author', 'group',)
# search_fields = ('text',)
# list_filter = ('pub_date',)
# list_editable = ('group',)
# empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year', 'rating',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
