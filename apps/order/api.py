from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import OrderSerializer
from apps.cart.models import CartItem


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)

        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=400)

        total = sum(item.product.price * item.quantity for item in cart_items)

        items = []
        for item in cart_items:
            items.append(
                {
                    "product": item.product.id,
                    "variant": (
                        item.selected_variant.id if item.selected_variant else None
                    ),
                    "shade": item.selected_shade.id if item.selected_shade else None,
                    "quantity": item.quantity,
                    "price": item.product.price,
                }
            )

        serializer = OrderSerializer(
            data={
                "user": request.user.id,
                "total_price": total,
                "shipping_address": request.data.get("shipping_address", "N/A"),
                "items": items,
            },
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Clear cart
        cart_items.delete()

        return Response(serializer.data, status=201)
