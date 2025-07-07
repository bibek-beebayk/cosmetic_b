from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.product.filters import ProductFilterSet

from .models import Brand, Product, ProductReview
from .serializers import (
    BrandSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductReviewSerializer,
)


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
        if self.action == "review":
            return ProductReviewSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"])
    def review(self, request, slug):
        user = request.user
        product = self.get_object()
        rating = request.data.get("rating", None)
        comment = request.data.get("comment", None)

        if rating is None and comment is None:
            return Response({"message": "Rating or comment are required"}, status=400)

        review, created = ProductReview.objects.get_or_create(
            user=user, product=product, defaults={"rating": rating, "comment": comment}
        )

        if not created:
            if not request.user == review.user:
                return Response(
                    {"message": "You are not allowed to update this review"}, status=403
                )
            review.rating = rating
            review.comment = comment
            review.save()
            return Response({"message": "Review updated successfully"})

        return Response({"message": "Review created successfully"})


class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"
    pagination_class = None
