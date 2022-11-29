from django_filters import rest_framework as dj_filters
from .models import Product


class ProductFilterSet(dj_filters.FilterSet):
    """Набор фильтров для представления для модели продуктов."""

    name = dj_filters.CharFilter(lookup_expr="icontains")
    category = dj_filters.CharFilter(field_name="category__name")

    order_by_field = "ordering"

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "category",
        ]
