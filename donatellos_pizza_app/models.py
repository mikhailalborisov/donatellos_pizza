from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings

from donatellos_pizza_app.managers import (
    AnnotatedManager,
    AnnotatedProductsInBasketManager,
)


# пользователь. можно использовать стандартную таблицу пользователей, как и их роли
#  class User(models.Model):
#      first_name = models.CharField(
#          max_length=100,
#          help_text="Введите имя с заглавной буквы",
#          verbose_name="Имя"
#      )
#      patronymic = models.CharField(
#          max_length=100,
#          help_text="Введите отчество",
#          verbose_name="Отчество",
#          null=True,
#          blank=True,
#      )
#      last_name = models.CharField(
#          max_length=100,
#          help_text="Введите фамилию",
#          verbose_name="Фамилия",
#      )
#      role = models.ForeignKey(
#          "Role",
#          on_delete=models.CASCADE,
#          help_text=" Выберите роль пользователя",
#          verbose_name="Роль пользователя",
#      )


# роль. Модели групп можно свои или стандартные
# class Role(models.Model):
#     name = models.CharField(
#         max_length=100,
#         help_text="Введите название роли",
#         verbose_name="Название роли"
#     )


# продукция. Меню блюда, имя, где категории блюда
class Product(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Введите название продукта",
        verbose_name="Название продукта",
    )
    price = models.PositiveIntegerField(
        help_text="Введите цену продукта", verbose_name="Цена продукта"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        help_text="Выберите категорию",
        verbose_name="Категория",
    )

    def __str__(self):
        return f"{self.name} ({self.category}) = {self.price}"


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Введите название категории",
        verbose_name="Название категории",
    )

    def __str__(self):
        return self.name


# Корзина. Пользователи только с ролью. Когда оплачено или нет, что представляет в модель
class Basket(models.Model):
    objects = AnnotatedManager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Выберите пользователя",
        verbose_name="Пользователь",
    )
    status = models.BooleanField(
        help_text="Введите статус заказа", verbose_name="Статус заказа", default=False
    )
    delivered_status = models.BooleanField(
        help_text="Введите статус доставки заказа",
        verbose_name="Статус доставки заказа",
        default=False,
    )
    address = models.CharField(
        max_length=100,
        default=None,
        blank=True,
        null=True,
        help_text="Введите адрес клиента",
        verbose_name="Адрес",
    )
    order_time = models.DateTimeField(
        help_text="Введите время заказа",
        default=None,
        blank=True,
        null=True,
        verbose_name="Время заказа",
    )
    delivery_time = models.DateTimeField(
        help_text="Указать ожидаемое время доставки",
        default=None,
        blank=True,
        null=True,
        verbose_name="Время доставки",
    )
    products = models.ManyToManyField(Product, through="ProductInBasket")

    def sum(self):
        pass


class ProductInBasket(models.Model):
    objects = AnnotatedProductsInBasketManager()

    basket = models.ForeignKey(
        "Basket", on_delete=models.CASCADE, related_name="products_in_basket",
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="baskets_for_product",
    )
    count = models.PositiveIntegerField(
        help_text="Количество", verbose_name="Количество"
    )


# Basket.objects.filter(products_in_basket__product=product_pk) # Найти все корзины у которых есть предмет с таким-то id (например все корзины с пиццей маргарита)
# Product.objects.filter(baskets_for_product__basket=basket_pk) # Найти все продукты которые есть в определенной корзине


# Склад. Заменить чек на корзину. Поле related_name - посмотреть в Google и проставить где нужно
class warehouse(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        help_text=" Выберите продукт",
        verbose_name="Продукт",
    )
    basket = models.ForeignKey(
        "Basket",
        on_delete=models.CASCADE,
        help_text=" Выберите чек",
        verbose_name="Чек",
    )
