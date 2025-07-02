from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    """
    A viewset for listing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    # pagination_class = None 
    lookup_field = 'slug' 

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return super().get_serializer_class()


    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category', None)
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset