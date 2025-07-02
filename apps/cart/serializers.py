from rest_framework import serializers
from apps.cart.models import WishListItem

class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = WishListItem
        fields = ['id', 'product', 'product_name', 'created_at']
