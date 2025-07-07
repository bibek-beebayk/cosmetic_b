from rest_framework import serializers

from apps.cart.models import WishListItem
from apps.product.models import (
    Category,
    Product,
    ProductImage,
    ProductProperty,
    ProductReview,
    ProductShade,
    ProductVariant,
)
from apps.users.serializers import UserSerializer


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product.brand.field.related_model
        fields = ["name", "logo", "slug"]


class CategorySerializer(serializers.ModelSerializer):
    # parent = CategorySerializer()
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "image", "parent"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image", "is_main"]


class ProductPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProperty
        fields = ["key", "value"]


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "name", "price", "sku", "stock", "image"]


class ProductShadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductShade
        fields = ["id", "name", "hex_code", "image", "sku", "stock"]
        read_only_fields = fields


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.name", read_only=True)
    image = serializers.SerializerMethodField()
    is_in_wishlist = serializers.SerializerMethodField()

    def get_is_in_wishlist(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return WishListItem.objects.filter(user=user, product=obj).exists()
        return False

    def get_image(self, obj):
        img = obj.images.filter(is_main=True).first()
        if img:
            img_url = self.context.get("request").build_absolute_uri(img.image.url)
            return img_url
        return None

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "slug",
            "rating",
            "brand",
            "is_in_wishlist",
        ]


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ProductReview
        exclude = ["product"]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    properties = ProductPropertySerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    shades = ProductShadeSerializer(many=True, read_only=True)
    is_in_wishlist = serializers.SerializerMethodField()
    reviews = ProductReviewSerializer(many=True, read_only=True)
    has_user_reviewed = serializers.SerializerMethodField()

    def get_has_user_reviewed(self, instance):
        user = self.context["request"].user
        if not user.pk:
            return False
        if ProductReview.objects.filter(user=user, product=instance).exists():
            return True
        return False

    def get_is_in_wishlist(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return WishListItem.objects.filter(user=user, product=obj).exists()
        return False

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "brand",
            "ingredients",
            "how_to_use",
            "price",
            "images",
            "rating",
            "properties",
            "variants",
            "shades",
            "is_in_wishlist",
            "reviews",
            "has_user_reviewed"
        ]
