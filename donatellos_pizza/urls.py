"""donatellos_pizza URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from donatellos_pizza_app.views import ProductViewSet, BasketViewSet, BasketItemsViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r"product", ProductViewSet, basename="product") #/product
router.register(r"basket", BasketViewSet, basename="basket") #/basket

basket_router = routers.NestedSimpleRouter(router, r'basket', lookup='basket')
basket_router.register(r'items', BasketItemsViewSet, basename='basket-items')


# drf-nested-routers https://github.com/alanjds/drf-nested-routers
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
    path("api/v1/", include(basket_router.urls)),
]
