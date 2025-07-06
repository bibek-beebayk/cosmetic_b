from rest_framework import serializers

from apps.cart.models import CartItem, WishListItem
from apps.product.serializers import (
    ProductListSerializer,
    ProductShadeSerializer,
    ProductVariantSerializer,
)


class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = WishListItem
        fields = ["id", "product", "product_name", "created_at"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    selected_variant = serializers.SerializerMethodField()
    selected_shade = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    def get_product_image(self, obj):
        img = None
        if obj.selected_shade and obj.selected_shade.image:
            img = obj.selected_shade.image
        elif obj.selected_variant and obj.selected_variant.image:
            img = obj.selected_variant.image
        else:
            img = obj.product.images.filter(is_main=True).first().image

        if img:
            img_url = self.context.get("request").build_absolute_uri(img.url)
            return img_url
        return None

    def get_selected_variant(self, obj):
        if obj.selected_variant:
            return obj.selected_variant.name
        return None

    def get_selected_shade(self, obj):
        if obj.selected_shade:
            return obj.selected_shade.name
        return None

    def get_price(self, obj):
        if obj.selected_variant:
            return obj.selected_variant.price
        # elif obj.selected_shade:
        #     return obj.selected_shade.price
        else:
            return obj.product.price

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "added_at",
            "selected_shade",
            "selected_variant",
            "price",
            "product_image",
        ]


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity", "selected_variant", "selected_shade"]

    def create(self, validated_data):
        # import ipdb; ipdb.set_trace()
        return super().create(validated_data)
