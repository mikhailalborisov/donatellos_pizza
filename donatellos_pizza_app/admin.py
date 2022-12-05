from django.contrib import admin

# Register your models here.

from .models import Product, Category, Basket, ProductInBasket

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Basket)
admin.site.register(ProductInBasket)
