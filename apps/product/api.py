from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.product.filters import ProductFilterSet

from .models import Product
from .serializers import ProductDetailSerializer, ProductListSerializer


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

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get("category", None)
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
