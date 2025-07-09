from django.contrib.auth import get_user_model
from django.db import models

from apps.product.models import Product, ProductShade, ProductVariant

User = get_user_model()


PAYMENT_OPTIONS = [("COD", "COD"), ("Esewa", "Esewa"), ("Khalti", "Khalti")]
STATUS_OPTIONS = [("pending", "Pending"), ("processing", "Processing"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    shipping_address = models.TextField()
    status = models.CharField(default="pending", max_length=20, choices=STATUS_OPTIONS)
    payment_method = models.CharField(
        default="COD", max_length=20, choices=PAYMENT_OPTIONS
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, null=True, blank=True, on_delete=models.SET_NULL
    )
    shade = models.ForeignKey(
        ProductShade, null=True, blank=True, on_delete=models.SET_NULL
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
