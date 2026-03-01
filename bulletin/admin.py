from django.contrib import admin
from .models import Category, Bulletin, Response

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Bulletin)
class BulletinAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('bulletin', 'author', 'created_at', 'accepted')
    list_filter = ('accepted', 'created_at')
    search_fields = ('text',)
    raw_id_fields = ('author', 'bulletin')
