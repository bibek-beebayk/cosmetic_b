from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "username", "phone", "is_staff", "is_active")
    search_fields = ("email", "username", "full_name")
    list_filter = ("is_staff", "is_active")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

