from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . models import User

# Register your models here.
@admin.register(User)
class AdminUser(UserAdmin):
    """AdminUser Model"""
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom profile", {
                "fields": (
                    "bio",
                    "gender",
                    "avatar",
                    "birthday",
                    "currency",
                    "language",
                    "superhost",
                )
            }
        ),
    )