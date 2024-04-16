from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewModel(admin.ModelAdmin):
    list_display = '__str__', 'avg_rating',
