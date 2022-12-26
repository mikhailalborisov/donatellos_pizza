import datetime
import re

from rest_framework import serializers

# from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from donatellos_pizza_app.models import Product, Category, Basket, ProductInBasket


class DeliveryTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ["delivery_time"]

    def validate_delivery_time(self, value):
        if not value:
            raise serializers.ValidationError("Время доставки должно быть указано")
        elif value < datetime.datetime.now(tz=datetime.timezone.utc):
            raise serializers.ValidationError("Время доставки должно быть позже текущего времени")
        return value


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ["address"]

    def validate_address(self, value):
        if not value:
            raise serializers.ValidationError("Время доставки должно быть указано")
        elif not bool(re.search(r'\d', value)) or not bool(re.search(r'[a-zA-Zа-яА-Я]', value)):
            raise serializers.ValidationError("Адрес должен содеражть название улицы и номер дома")
        return value


class BasketSerializer(serializers.ModelSerializer):
    total_sum = serializers.IntegerField(default=0)

    class Meta:
        model = Basket
        fields = "__all__"


class BasketItemsSerializer(serializers.ModelSerializer):
    item_cost = serializers.IntegerField(read_only=True, default=0, allow_null=True)

    class Meta:
        model = ProductInBasket
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор по модели Product."""

    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ("id", "name", "price", "category")


class PaymentSerializer(AddressSerializer, DeliveryTimeSerializer, BasketSerializer):
    class Meta:
        model = Basket
        fields = "__all__"

    def validate_status(self, value):
        if value:
            raise serializers.ValidationError("Заказ уже оплачен")
        return value

    def validate_total_sum(self, value):
        if not value:
            raise serializers.ValidationError("Корзина пустая")
        elif value <= 0:
            raise serializers.ValidationError("Корзина пустая")
