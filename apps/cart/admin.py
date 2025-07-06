from django.contrib import admin
from .models import WishListItem, CartItem


@admin.register(WishListItem)
class WishListItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    search_fields = ("user__username", "product__name")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user", "product")
    

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "added_at")
    search_fields = ("user__username", "product__name")
    list_filter = ("added_at",)
    ordering = ("-added_at",)
