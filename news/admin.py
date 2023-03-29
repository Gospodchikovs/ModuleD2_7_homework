from django.contrib import admin
from .models import Post, Author, Category, PostCategory, Comment, Subscriber


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
    nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'type', 'time_create', 'get_author', 'heading', 'body', 'rating')
    search_fields = ('heading', 'body')
    list_filter = ('type', 'heading', 'author')
    actions = [nullfy_rating]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'id')


class AuthorAdmin(admin.ModelAdmin):
    list_display =('user', 'rating')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'comment', 'time_create', 'rating')
    search_fields = ('user', 'comment')
    list_filter = ('user', 'rating')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    search_fields = ('post', 'category')


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    search_fields = ('user', 'category')
    list_filter = ('user', 'category')


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
