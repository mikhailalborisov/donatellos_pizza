from rest_framework import serializers
from django.utils import timezone
from donatellos_pizza_app.models import Product, Category, Basket


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
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
