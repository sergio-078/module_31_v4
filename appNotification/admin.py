from django.contrib import admin
from .models import Post, Response, News, Category, Subscription

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'is_accepted', 'is_rejected']
    list_filter = ['is_accepted', 'is_rejected', 'created_at']
    list_editable = ['is_accepted', 'is_rejected']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'views_count', 'notify_subscribers']
    list_filter = ['created_at', 'notify_subscribers']
    list_editable = ['notify_subscribers']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'news', 'created_at']
    list_filter = ['news', 'created_at']

