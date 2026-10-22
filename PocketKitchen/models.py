from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)    
    name = models.CharField(max_length=200)
    options=(
        ("Appetizers","Appetizers"),
        ("Desserts","Desserts"),
        ("Snacks","Snacks"),
        ("Juice","Juice"),
        ("Salad","Salad"),
        ("Bakes","Bakes"),
        ("Breakfast","Breakfast"),
        ("Veg","Veg"),
        ("Non-veg","Non-veg"),
        ("Seafood","Seafood"),
        ("Other","Other"),
    )
    category = models.CharField(max_length=100,choices=options)
    description = models.TextField(max_length=1000)
    ingredients = models.TextField(help_text="List ingredients separated by commas.")
    instructions = models.TextField(help_text="Detailed instructions for preparing the recipe.")
    image = models.ImageField(upload_to='recipe_images/', blank=True,default=1)
    cook_time = models.PositiveIntegerField(help_text="Cooking time in minutes.")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.name
    
    def count_likes(self):
        return self.likes.count()

class RecipeVideo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)    
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    video = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='comments',default=1)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def _str_(self):
        return f"Comment by {self.user.username}"
    
    @property
    def like_count(self):
        return self.likes.count()
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    