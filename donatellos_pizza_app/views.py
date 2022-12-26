from .serializers import (
    ProductSerializer,
    BasketSerializer,
    BasketItemsSerializer,
    AddressSerializer,
    DeliveryTimeSerializer, PaymentSerializer,
)
from donatellos_pizza_app.models import Product, Basket, ProductInBasket
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
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

    @action(methods=["GET"], detail=True, url_path="address", url_name="address")
    def address(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data["address"])

    @address.mapping.post
    @address.mapping.patch
    def set_address(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            instance.set_address(serializer.validated_data["address"])
            instance.save()
            return Response({"status": "address set"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["GET"], detail=True, url_path="delivery_time", url_name="delivery_time"
    )
    def delivery_time(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data["delivery_time"])

    @delivery_time.mapping.post
    @delivery_time.mapping.patch
    def set_delivery_time(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeliveryTimeSerializer(data=request.data)
        if serializer.is_valid():
            instance.set_delivery_time(serializer.validated_data["delivery_time"])
            instance.save()
            return Response({"delivered_status": "delivery_time set"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"], detail=True, url_path="payment", url_name="payment"
    )
    def payment(self, request, *args, **kwargs):
        instance = self.get_object()
        object_data = BasketSerializer(instance).data
        serializer = PaymentSerializer(data=object_data)
        if serializer.is_valid():
            instance.payment()
            instance.save()
            return Response(BasketSerializer(instance).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        busket = Basket.objects.filter(user=user.pk, id=basket_pk).first()
        if busket:
            if not busket.status:
                request.data["basket"] = self.kwargs["basket_pk"]
                ret = super().create(request, *args, **kwargs)
                return ret
            else:
                return Response({"Заказ выкуплен"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"404"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        user = request.user
        basket_pk = self.kwargs.get("basket_pk")
        busket = Basket.objects.filter(user=user.pk, id=basket_pk).first()
        if busket:
            if not busket.status:
                if ProductInBasket.objects.filter(
                        basket=basket_pk, id=self.kwargs["pk"]
                ).exists():
                    if request.data["count"] == 0:
                        pass  # delete entity, return
                    request.data["basket"] = self.kwargs["basket_pk"]
                    ret = super().update(request, *args, **kwargs)
                    return ret
                else:
                    # create entity
                    pass
            else:
                return Response({"Заказ выкуплен"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"404"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        basket_pk = self.kwargs.get("basket_pk")

        busket = Basket.objects.filter(user=user.pk, id=basket_pk).first()
        if busket:
            if not busket.status:
                if ProductInBasket.objects.filter(
                        basket=basket_pk, id=self.kwargs["pk"]
                ).exists():
                    ret = super().destroy(request, *args, **kwargs)
                    return ret
            else:
                return Response({"Заказ выкуплен"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"404"}, status=status.HTTP_404_NOT_FOUND)
