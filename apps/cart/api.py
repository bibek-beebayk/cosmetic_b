from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.product.models import Product
from apps.cart.models import WishListItem
from apps.cart.serializers import WishlistSerializer
from apps.product.serializers import ProductListSerializer

class WishlistViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        wishlist = WishListItem.objects.filter(user=request.user).values_list("product__id", flat=True)
        # import ipdb; ipdb.set_trace()
        wishlist_products = Product.objects.filter(id__in=wishlist)
        serializer = ProductListSerializer(wishlist_products, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'Product ID required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item, created = WishListItem.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            return Response({'message': 'Removed from wishlist'}, status=status.HTTP_200_OK)

        return Response({'message': 'Added to wishlist'}, status=status.HTTP_201_CREATED)
