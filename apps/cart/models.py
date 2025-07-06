from django.contrib.auth import get_user_model
from django.db import models
from apps.product.models import Product, ProductShade, ProductVariant

User = get_user_model()


class WishListItem(models.Model):
    user = models.ForeignKey(
        User,
        related_name="wishlist_items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name="wishlist_items",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist item for {self.product.name} by {self.user.username}"

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_shade = models.ForeignKey(
        ProductShade, on_delete=models.SET_NULL, null=True, blank=True
    )
    selected_variant = models.ForeignKey(
        ProductVariant, on_delete=models.SET_NULL, null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ("user", "product", "selected_variant"),
            ("user", "product", "selected_shade"),
        ]
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.quantity})"
