from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from .models import *

class LoginForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))

class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control"}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
        }
        
class RecipeForm(forms.ModelForm):
    class Meta:
        model=Recipe
        fields = [
            'name',
            'category',
            'description',
            'ingredients',
            'instructions',
            'image',
            'cook_time',
        ]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Recipe Name"}),
            "category":forms.Select(attrs={"class":"form-select"}),
            "description":forms.Textarea(attrs={"class":"form-control","placeholder":"Recipe Description"}),
            "ingredients":forms.Textarea(attrs={"class":"form-control","placeholder":"List the Ingredients"}),
            "instructions":forms.Textarea(attrs={"class":"form-control","placeholder":"Step-by-Step Instructions"}),
            "cook_time":forms.TextInput(attrs={"class":"form-control","placeholder":"Cooking Time in Minutes"}),
        }

class RecipeVideoForm(forms.ModelForm):
    class Meta:
        model=RecipeVideo
        fields=['title','caption','video']
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "caption":forms.Textarea(attrs={"class":"form-control"}),
            "video":forms.FileInput(attrs={"class":"form-control"}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Enter your feedback here...'}),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Write your Comment'}),
        }

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your email", max_length=200, required=True)