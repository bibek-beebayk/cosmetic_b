from django.contrib import admin

from .models import Brand, Category, Product, ProductImage, ProductProperty, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_filter = ("parent",)
    ordering = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "brand", "sku", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug", "sku")
    list_filter = ("category", "brand")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProductImageInline, ProductPropertyInline]


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    search_fields = ("product__name", "user__username")
    list_filter = ("rating", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
