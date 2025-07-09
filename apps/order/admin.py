from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ["id", "user", "total_price", "is_paid", "status", "created_at"]
    list_filter = ["is_paid", "status"]
    ordering = ["created_at", "total_price"]
