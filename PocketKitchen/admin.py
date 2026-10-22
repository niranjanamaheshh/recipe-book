from django.contrib import admin
from .models import *
from .models import Feedback

# @admin.register(Feedback)
# class FeedbackAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'subject', 'submitted_at')
#     search_fields = ('name', 'email', 'subject', 'message')

# Register your models here.
admin.site.register(Recipe)
admin.site.register(RecipeVideo)
admin.site.register(Feedback)