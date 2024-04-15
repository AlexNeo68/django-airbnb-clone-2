from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewModel(admin.ModelAdmin):
    pass
