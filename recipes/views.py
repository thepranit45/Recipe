# recipes\views.py - COMPLETE VERSION

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Recipe, Category, Rating
from .forms import RecipeForm, RatingForm

class RecipeListView(ListView):
    """Shows all recipes in a nice grid"""
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12  # Show 12 recipes per page
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(ingredients__icontains=search_query)
            )
        
        # Category filter
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        # Difficulty filter
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['current_difficulty'] = self.request.GET.get('difficulty')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class RecipeDetailView(ListView):
    """Shows a single recipe with all details and ratings"""
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'ratings'
    paginate_by = 10
    
    def get_queryset(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        return Rating.objects.filter(recipe=recipe)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        context['recipe'] = recipe
        context['rating_form'] = RatingForm()
        return context

class RecipeCreateView(SuccessMessageMixin, CreateView):
    """Page to create a new recipe"""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_message = "Recipe '%(title)s' created successfully!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

class RecipeUpdateView(SuccessMessageMixin, UpdateView):
    """Page to edit an existing recipe"""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    success_message = "Recipe '%(title)s' updated successfully!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

class RecipeDeleteView(SuccessMessageMixin, DeleteView):
    """Page to delete a recipe"""
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')
    success_message = "Recipe deleted successfully!"

def add_rating(request, pk):
    """Handle adding a rating to a recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.recipe = recipe
            rating.save()
            messages.success(request, 'Thank you for your rating!')
        else:
            messages.error(request, 'Please correct the errors below.')
    return redirect('recipe_detail', pk=pk)

class CategoryListView(ListView):
    """Shows all categories"""
    model = Category
    template_name = 'recipes/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(SuccessMessageMixin, CreateView):
    """Page to create a new category"""
    model = Category
    fields = ['name', 'description']
    template_name = 'recipes/category_form.html'
    success_url = reverse_lazy('category_list')
    success_message = "Category created successfully!"
