# recipes\admin.py

from django.contrib import admin
from .models import Recipe, Category, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty_level', 'prep_time', 'cook_time', 'created_at']
    list_filter = ['category', 'difficulty_level', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'rating', 'reviewer_name', 'created_at']
    list_filter = ['rating', 'created_at']
