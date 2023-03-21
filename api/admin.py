from django.contrib import admin

from api.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'description', 'image', 'content', 'like']
