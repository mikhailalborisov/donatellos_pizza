"""donatellos_pizza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from donatellos_pizza_app.views import ProductViewSet, BasketViewSet

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product") #/product
router.register(r"basket", BasketViewSet, basename="basket") #/basket


# drf-nested-routes https://github.com/alanjds/drf-nested-routers
#/basket/<basket_id>/items
#/basket/<basket_id>/items/<item_id>

# {"product_id" : 10, "count" : 1}


# {"basket" : 12, "products" : [{name: name, price: price, ...},{name: name, price: price, ...},]}

# работать только с одним заказом одновременно - переопределение query set
# работать только со своим заказом - достать пользователя из данных по запросу - permission_classes = (IsAuthenticated, )

# POST /basket/<basket_id>/items [авторизация] - добавлять в свой заказ блюда из меню пиццерии
# GET /basket/<basket_id>/items [авторизация] - смотреть блюда из своего текущего заказа
# PATCH /basket/<basket_id>/items/<item_id> {count} [авторизация] - редактировать количество каждого из блюд в заказ
# DELETE /basket/<basket_id>/items/<item_id> [авторизация] - убирать блюдо из заказа


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
]
