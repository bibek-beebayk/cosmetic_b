from django_filters import FilterSet, AllValuesFilter, NumberFilter, CharFilter

from apps.product.models import Product


class ProductFilterSet(FilterSet):
    category = AllValuesFilter(field_name="category__name")
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    sort = CharFilter(
        method="sort_queryset",
        label="Sort by",
    )


    def sort_queryset(self, queryset, name, value):
        if value == "price_asc":
            return queryset.order_by("price")
        elif value == "price_desc":
            return queryset.order_by("-price")
        elif value == "name_asc":
            return queryset.order_by("name")
        elif value == "name_desc":
            return queryset.order_by("-name")
        return queryset

    class Meta:
        model = Product
        fields = [
            "category",
            "min_price",
            "max_price",
            "sort",
        ]