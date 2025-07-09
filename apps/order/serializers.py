from rest_framework import serializers

from apps.product.serializers import ProductListSerializer, ProductShadeSerializer, ProductVariantSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField(read_only=True)
    variant_data = serializers.SerializerMethodField(read_only=True)
    shade_data = serializers.SerializerMethodField(read_only=True)

    def get_variant_data(self, obj):
        if obj.variant:
            return ProductVariantSerializer(
                obj.variant, context={"request": self.context.get("request")}
            ).data
        return None
    
    def get_shade_data(self, obj):
        if obj.shade:
            return ProductShadeSerializer(
                obj.shade, context={"request": self.context.get("request")}
            ).data
        return None

    def get_product_data(self, obj):
        # import ipdb; ipdb.set_trace()
        return ProductListSerializer(
            obj.product, context={"request": self.context.get("request")}
        ).data

    class Meta:

        model = OrderItem
        fields = [
            "id",
            "product",
            "product_data",
            "variant",
            "shade",
            "quantity",
            "price",
            "variant_data",
            "shade_data"
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "created_at",
            "total_price",
            "shipping_address",
            "is_paid",
            "status",
            "items",
            "payment_method",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
