from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings

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
    cheque = models.ForeignKey(
        "Cheque",
        on_delete=models.CASCADE,
        help_text=" Выберите чек",
        verbose_name="Чек",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Выберите пользователя",
        verbose_name="Пользователь",
    )


# Чек. Добавить пользователя с ролью доставки.
# Нужно добавить адрес, ожидаемое время доставки. Выполнена доставка. Добавить время заказа
class Cheque(models.Model):
    sum = models.PositiveIntegerField(
        help_text="Введите сумму чека", verbose_name="Сумма чека"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=" Выберите пользователя",
        verbose_name="Пользователь",
    )
    address = models.CharField(
        max_length=100, help_text="Введите адрес клиента", verbose_name="Адрес"
    )
    order_time = models.DateTimeField(
        help_text="Введите время заказа", verbose_name="Время заказа"
    )
    delivery_time = models.DateTimeField(
        help_text="Введите время доставки", verbose_name="Время доставки"
    )


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
