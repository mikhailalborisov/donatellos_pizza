from .serializers import ProductSerializer, BasketSerializer
from donatellos_pizza_app.models import Product, Basket
from rest_framework import viewsets, mixins


# Create your views here.
class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.all().order_by("-id")

    def get_serializer_class(self):
        return ProductSerializer


class BasketiewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Basket.objects.all().order_by("-id")

    serializer_class = BasketSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        request.data["user"] = user.pk
        ret = super().create(request, *args, **kwargs)
        return ret
