from django.contrib import admin
from .models import Blog, BlogSection


class BlogSectionInline(admin.StackedInline):
    model = BlogSection
    extra = 0
    fields = ("title", "content", "image", "order")
    # readonly_fields = ("order",)
    ordering = ("order",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug", "author")
    list_filter = ("author",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [BlogSectionInline]
