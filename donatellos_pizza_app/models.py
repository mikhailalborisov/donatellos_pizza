from django.db import models


# пользователь
class User(models.Model):
    first_name = models.CharField(
        max_length=100,
        help_text="Введите имя с заглавной буквы",
        verbose_name="Имя"
    )
    patronymic = models.CharField(
        max_length=100,
        help_text="Введите отчество",
        verbose_name="Отчество",
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=100,
        help_text="Введите фамилию",
        verbose_name="Фамилия",
    )
    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE,
        help_text=" Выберите роль пользователя",
        verbose_name="Роль пользователя",
    )


# роль
class Role(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Введите название роли",
        verbose_name="Название роли"
    )


# продукция
class Product(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Введите название продукта",
        verbose_name="Название продукта"
    )
    price = models.PositiveIntegerField(
        help_text="Введите цену продукта",
        verbose_name="Цена продукта"
    )


# корзина
class Basket(models.Model):
    cheque = models.ForeignKey(
        "Cheque",
        on_delete=models.CASCADE,
        help_text=" Выберите чек",
        verbose_name="Чек",
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        help_text=" Выберите пользователя",
        verbose_name="Пользователь",
    )


# чек
class Cheque(models.Model):
    sum = models.PositiveIntegerField(
        help_text="Введите сумму чека",
        verbose_name="Сумма чека"
    )


# склад
class warehouse(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        help_text=" Выберите продукт",
        verbose_name="Продукт",
    )
    cheque = models.ForeignKey(
        "Cheque",
        on_delete=models.CASCADE,
        help_text=" Выберите чек",
        verbose_name="Чек",
    )
