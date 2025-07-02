from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.siteconfig import api as siteconfig_api
from apps.product import api as product_api
from apps.users import api as user_api

router = DefaultRouter()

router.register("product", product_api.ProductViewSet, basename="product")
router.register("auth", user_api.AuthenticationViewSet, basename="auth")
router.register("user", user_api.UserViewSet, basename="user")
# router.register("collection", product_api.CollectionViewSet, basename="collection")
# router.register("order", order_api.OrderViewSet, basename="order")
# router.register("category", categoty_api.CategoryViewSet, basename="category")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/home/", siteconfig_api.HomePageView.as_view()),
    path("api/v1/navitems/", siteconfig_api.NavItemView.as_view()),
    # path("deploy/", order_api.DeployView.as_view())
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
