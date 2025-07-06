from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.cart.models import CartItem, WishListItem
from apps.cart.serializers import (
    AddToCartSerializer,
    CartItemSerializer,
    WishlistSerializer,
)
from apps.product.models import Product
from apps.product.serializers import ProductListSerializer


class WishlistViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        wishlist = WishListItem.objects.filter(user=request.user).values_list(
            "product__id", flat=True
        )
        # import ipdb; ipdb.set_trace()
        wishlist_products = Product.objects.filter(id__in=wishlist)
        serializer = ProductListSerializer(
            wishlist_products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {"error": "Product ID required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        wishlist_item, created = WishListItem.objects.get_or_create(
            user=request.user, product=product
        )

        if not created:
            wishlist_item.delete()
            return Response(
                {"message": "Removed from wishlist"}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Added to wishlist"}, status=status.HTTP_201_CREATED
        )


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data.get("quantity", 1)
        selected_shade = serializer.validated_data.get("selected_shade")
        selected_variant = serializer.validated_data.get("selected_variant")

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            selected_shade=selected_shade,
            selected_variant=selected_variant,
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return cart_item

    def get_serializer_class(self):
        if self.action == "add":
            return AddToCartSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["post"])
    def add(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        selected_shade = request.data.get("selected_shade")
        selected_variant = request.data.get("selected_variant")

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        serializer = self.get_serializer(
            data={
                "product": product_id,
                "quantity": quantity,
                "selected_shade": selected_shade,
                "selected_variant": selected_variant,
            }
        )
        serializer.is_valid(raise_exception=True)
        # import ipdb

        # ipdb.set_trace()
        self.perform_create(serializer)
        return Response({"message": "Added to cart"}, status=201)

    # @action(detail=True, methods=["post"])
    # def remove(self, request):
    #     product_id = request.data.get("product_id")

    #     if not product_id:
    #         return Response({"error": "Product ID is required"}, status=400)

    #     try:
    #         cart_item = CartItem.objects.get(user=request.user, product__id=product_id)
    #     except CartItem.DoesNotExist:
    #         return Response({"error": "Product not found in cart"}, status=404)

    #     cart_item.delete()
    #     return Response({"message": "Removed from cart"}, status=200)

    @action(detail=True, methods=["patch"], url_path="update-quantity")
    def update_quantity(self, request, pk=None):
        quantity = request.data.get("quantity")
        if quantity is None or int(quantity) <= 0:
            return Response({"error": "Quantity must be greater than 0"}, status=400)

        cart_item = self.get_object()
        cart_item.quantity = quantity
        cart_item.save()
        return Response({"message": "Quantity updated"}, status=200)
