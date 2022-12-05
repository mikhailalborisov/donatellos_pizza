# Generated by Django 4.1.3 on 2022-11-29 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Basket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название категории",
                        max_length=100,
                        verbose_name="Название категории",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название продукта",
                        max_length=100,
                        verbose_name="Название продукта",
                    ),
                ),
                (
                    "price",
                    models.PositiveIntegerField(
                        help_text="Введите цену продукта", verbose_name="Цена продукта"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text=" Выберите категорию",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="donatellos_pizza_app.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="warehouse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "basket",
                    models.ForeignKey(
                        help_text=" Выберите чек",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="donatellos_pizza_app.basket",
                        verbose_name="Чек",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text=" Выберите продукт",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="donatellos_pizza_app.product",
                        verbose_name="Продукт",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cheque",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sum",
                    models.PositiveIntegerField(
                        help_text="Введите сумму чека", verbose_name="Сумма чека"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        help_text="Введите адрес клиента",
                        max_length=100,
                        verbose_name="Адрес",
                    ),
                ),
                (
                    "order_time",
                    models.DateTimeField(
                        help_text="Введите время заказа", verbose_name="Время заказа"
                    ),
                ),
                (
                    "delivery_time",
                    models.DateTimeField(
                        help_text="Введите время доставки",
                        verbose_name="Время доставки",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text=" Выберите пользователя",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="basket",
            name="cheque",
            field=models.ForeignKey(
                blank=True,
                help_text=" Выберите чек",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="donatellos_pizza_app.cheque",
                verbose_name="Чек",
            ),
        ),
        migrations.AddField(
            model_name="basket",
            name="user",
            field=models.ForeignKey(
                help_text="Выберите пользователя",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
