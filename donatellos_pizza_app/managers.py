from django.db.models import F, Sum, Manager, QuerySet
from django.db.models.functions import Coalesce


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
            total_sum=Coalesce(Sum(F("products__price") * F("products_in_basket__count")), 0)
        )

        return qs
