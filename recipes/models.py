# recipes\models.py

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Categories for recipes like Breakfast, Lunch, Desserts"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"  # Shows "Categories" not "Categorys"
    
    def __str__(self):
        return self.name  # When you print a category, show its name

class Recipe(models.Model):
    """Main Recipe model with all recipe information"""
    
    # Difficulty choices
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    # Basic recipe information
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text="List ingredients, one per line")
    instructions = models.TextField(help_text="Step-by-step cooking instructions")
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Time and serving information
    prep_time = models.PositiveIntegerField(help_text="Preparation time in minutes")
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    servings = models.PositiveIntegerField(default=1)
    difficulty_level = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    
    # Automatically track when recipe was created/updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Show newest recipes first
    
    def __str__(self):
        return self.title  # When you print a recipe, show its title
    
    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})
    
    @property
    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time
    
    @property
    def average_rating(self):
        """Calculate average rating for this recipe"""
        ratings = self.rating_set.all()
        if ratings:
            return round(sum([rating.rating for rating in ratings]) / len(ratings), 1)
        return 0

class Rating(models.Model):
    """User ratings and reviews for recipes"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]  # 1-5 stars
    )
    review_text = models.TextField(blank=True)
    reviewer_name = models.CharField(max_length=100, default="Anonymous")
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Show newest ratings first
    
    def __str__(self):
        return f"{self.rating} stars for {self.recipe.title}"
