from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blog.models import Blog
from apps.product.models import Product
from apps.product.serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductListSerializer,
)
from apps.siteconfig.serializers import BannerSerializer

from .models import Banner


class HomePageView(APIView):

    def get(self, request):
        banners = Banner.objects.filter(active=True).order_by("-created_at")[:3]
        banner_data = BannerSerializer(
            banners, many=True, context={"request": request}
        ).data

        new_arrivals = Product.get_new_arrivals(limit=4)
        new_arrivals_data = ProductListSerializer(
            new_arrivals, many=True, context={"request": request}
        ).data

        best_sellers = Product.get_best_sellers(limit=4)
        best_sellers_data = ProductListSerializer(
            best_sellers, many=True, context={"request": request}
        ).data

        brands = Product.brand.field.related_model.objects.all()[:6]
        brand_data = BrandSerializer(
            brands, many=True, context={"request": request}
        ).data

        categories = Product.category.field.related_model.objects.all()[:6]
        category_data = CategorySerializer(
            categories, many=True, context={"request": request}
        ).data

        blogs = Blog.objects.all()[:3]  # Assuming you want to fetch blogs as well
        

        res = {
            "banners": banner_data,
            "new_arrivals": new_arrivals_data,
            "best_sellers": best_sellers_data,
            "brands": brand_data,
            "categories": category_data,
        }
        return Response(res, status=200)
