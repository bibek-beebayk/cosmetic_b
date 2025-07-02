from django_filters import AllValuesFilter, CharFilter, FilterSet, NumberFilter

from apps.product.models import Product


class ProductFilterSet(FilterSet):
    # category = AllValuesFilter(field_name="category__name")
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    sort = CharFilter(
        method="sort_queryset",
        label="Sort by",
    )

    category = CharFilter(
        method="filter_by_category",
        label="Category Filter",
    )

    def filter_by_category(self, queryset, name, value):
        if value == "all":
            return queryset
        else:
            return queryset.filter(category__slug__iexact=value)

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
