from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# router.register("product", product_api.ProductViewSet, basename="product")
# router.register("collection", product_api.CollectionViewSet, basename="collection")
# router.register("order", order_api.OrderViewSet, basename="order")
# router.register("category", categoty_api.CategoryViewSet, basename="category")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # path("api/home/", product_api.HomePageView.as_view()),
    # path("deploy/", order_api.DeployView.as_view())
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
