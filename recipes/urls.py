# recipes\urls.py (CREATE THIS FILE)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipe/<int:pk>/rate/', views.add_rating, name='add_rating'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
]
