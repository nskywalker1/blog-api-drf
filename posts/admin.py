from django.contrib import admin
from .models import Post, Tag, Category, Comment

admin.site.register(Post)


class PostAdmin(admin.ModelAdmin):
    list_display = '__all__'
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = '__all__'
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category)


class Categorydmin(admin.ModelAdmin):
    list_display = '__all__'
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Comment)
