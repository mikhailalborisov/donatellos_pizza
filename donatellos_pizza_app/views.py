from .serializers import ProductSerializer, BasketSerializer, BasketItemsSerializer
from donatellos_pizza_app.models import Product, Basket, ProductInBasket
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .filters import ProductFilterSet


# Create your views here.
class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.all().order_by("-id")
    filterset_class = ProductFilterSet

    def get_serializer_class(self):
        return ProductSerializer


class BasketViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    # queryset = Basket.objects.all().order_by("-id") #.filter(user=...) <достать пользователя из данных по запросу>

    serializer_class = BasketSerializer

    def get_queryset(self):
        user = self.request.user
        return Basket.objects.filter(user=user.pk).order_by("-id")

    def create(self, request, *args, **kwargs):
        user = request.user
        request.data["user"] = user.pk
        ret = super().create(request, *args, **kwargs)
        return ret


class BasketItemsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = BasketItemsSerializer

    def get_queryset(self):
        user = self.request.user
        return ProductInBasket.objects.filter(
            basket__user=user.pk, basket=self.kwargs["basket_pk"]
        ).order_by("-id")

    def create(self, request, *args, **kwargs):
        user = request.user
        basket_pk = self.kwargs["basket_pk"]
        if Basket.objects.filter(user=user.pk, id=basket_pk).exists():
            request.data["basket"] = self.kwargs["basket_pk"]
            ret = super().create(request, *args, **kwargs)
            return ret
