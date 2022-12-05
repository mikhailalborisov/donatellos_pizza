from .serializers import ProductSerializer, BasketSerializer, BasketItemsSerializer
from donatellos_pizza_app.models import Product, Basket, ProductInBasket
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from .filters import ProductFilterSet
from rest_framework.response import Response


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


class BasketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    # queryset = Basket.objects.all().order_by("-id") #.filter(user=...) <достать пользователя из данных по запросу>

    serializer_class = BasketSerializer

    def get_queryset(self):
        user = self.request.user
        return Basket.objects.filter(user=user.pk).order_by("-id")

    def create(self, request, *args, **kwargs):
        user = request.user
        request.data["user"] = user.pk

        current_basket = Basket.objects.filter(user=user.pk, status=False)
        if len(current_basket) == 0:
            ret = super().create(request, *args, **kwargs)
            return ret
        else:
            serializer = self.get_serializer(current_basket[0])
            return Response(serializer.data)


# from django.db.models import F, Sum


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
        basket_pk = self.kwargs.get("basket_pk")
        if Basket.objects.filter(user=user.pk, id=basket_pk).exists():
            request.data["basket"] = self.kwargs["basket_pk"]
            ret = super().create(request, *args, **kwargs)
            return ret
        return Response({"404"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        user = request.user
        basket_pk = self.kwargs.get("basket_pk")
        if Basket.objects.filter(user=user.pk, id=basket_pk).exists():
            if ProductInBasket.objects.filter(
                basket=basket_pk, id=self.kwargs["pk"]
            ).exists():
                if request.data["count"] == 0:
                    pass  # delete entity, return
                request.data["basket"] = self.kwargs["basket_pk"]
                ret = super().update(request, *args, **kwargs)
                return ret
        return Response({"404"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        basket_pk = self.kwargs.get("basket_pk")
        if Basket.objects.filter(user=user.pk, id=basket_pk).exists():
            if ProductInBasket.objects.filter(
                basket=basket_pk, id=self.kwargs["pk"]
            ).exists():
                ret = super().destroy(request, *args, **kwargs)
                return ret
        return Response({"404"}, status=status.HTTP_404_NOT_FOUND)
