from django_filters import FilterSet, AllValuesFilter, NumberFilter, CharFilter

from apps.product.models import Product


class ProductFilterSet(FilterSet):
    category = AllValuesFilter(field_name="category__name")
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")
    # Option 1: Using CharFilter (accepts any string value)
    sort = CharFilter(
        method="sort_queryset",
        label="Sort by",
    )
    
    # Option 2: Using ChoiceFilter (restricts to specific choices)
    # sort = ChoiceFilter(
    #     method="sort_queryset",
    #     label="Sort by",
    #     choices=[
    #         ("price_asc", "Price: Low to High"),
    #         ("price_desc", "Price: High to Low"),
    #         ("name_asc", "Name: A to Z"),
    #         ("name_desc", "Name: Z to A"),
    #     ],
    # )

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
            "sort",  # Add sort to fields
        ]