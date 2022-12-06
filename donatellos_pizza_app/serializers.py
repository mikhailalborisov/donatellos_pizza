from rest_framework import serializers

# from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from donatellos_pizza_app.models import Product, Category, Basket, ProductInBasket


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ["address"]

    def validate_address(self, value):
        if value != value.capitalize():
            raise serializers.ValidationError("Название должно быть с заглавной буквы")
        return value

class BasketSerializer(serializers.ModelSerializer):
    total_sum = serializers.IntegerField()

    class Meta:
        model = Basket
        fields = "__all__"


class BasketItemsSerializer(serializers.ModelSerializer):
    item_cost = serializers.IntegerField()

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
