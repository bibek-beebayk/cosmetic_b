from django.contrib.auth import get_user_model
from django.db import models
from apps.product.models import Product

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
        unique_together = ('user', 'product')
        ordering = ['-created_at']
