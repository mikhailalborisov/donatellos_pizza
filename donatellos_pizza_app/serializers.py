from rest_framework import serializers

# from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from donatellos_pizza_app.models import Product, Category, Basket, ProductInBasket


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
