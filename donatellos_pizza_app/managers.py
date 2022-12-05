from django.db.models import F, Sum, Manager
from django.db.models import QuerySet


class AnnotatedProductsInBasketManager(Manager):
    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        qs = qs.prefetch_related("product")
        qs = qs.annotate(item_cost=F("product__price") * F("count"))

        return qs


class AnnotatedManager(Manager):
    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()

        qs = qs.prefetch_related("products_in_basket")
        qs = qs.prefetch_related("products")
        qs = qs.annotate(
            total_sum=Sum(F("products__price") * F("products_in_basket__count"))
        )

        return qs
