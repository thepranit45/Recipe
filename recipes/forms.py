# recipes\forms.py (CREATE THIS FILE)

from django import forms
from .models import Recipe, Category, Rating

class RecipeForm(forms.ModelForm):
    """Form for creating and editing recipes"""
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'ingredients', 'instructions', 
                 'image', 'prep_time', 'cook_time', 'servings', 'difficulty_level']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of your recipe'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': '• 2 cups flour\n• 1 cup sugar\n• 3 eggs'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '1. Preheat oven to 350°F\n2. Mix ingredients...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Minutes'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1',
                'placeholder': 'Minutes'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of servings'
            }),
            'difficulty_level': forms.Select(attrs={'class': 'form-select'}),
        }

class RatingForm(forms.ModelForm):
    """Form for rating recipes"""
    
    class Meta:
        model = Rating
        fields = ['rating', 'review_text', 'reviewer_name']
        
        widgets = {
            'rating': forms.Select(choices=[(i, '⭐' * i) for i in range(1, 6)], attrs={
                'class': 'form-select'
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts about this recipe...'
            }),
            'reviewer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)'
            })
        }
