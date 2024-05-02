from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . models import User

# Register your models here.
@admin.register(User)
class AdminUser(UserAdmin):
    """AdminUser Model"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'email_verified', 'login_type',)

    list_filter = UserAdmin.list_filter + ('superhost',)

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
                    "login_type",
                )
            }
        ),
    )