from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.product.filters import ProductFilterSet

from .models import Brand, Product
from .serializers import BrandSerializer, ProductDetailSerializer, ProductListSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = "slug"
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter]
    search_fields = ["name", "category__name", "brand__name"]
    filterset_class = ProductFilterSet

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return super().get_serializer_class()


class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"
    pagination_class = None
