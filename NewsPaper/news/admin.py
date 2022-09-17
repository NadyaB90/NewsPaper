from django.contrib import admin
from .models import Post, Author, Category, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category_type', 'title', 'text', 'post_rate', 'created_date')
    list_filter = ('author', 'category_type', 'title', 'post_rate', 'created_date')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
