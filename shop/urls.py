from django.urls import path, include, reverse_lazy

from shop.views import create_shop_view, my_shop_view, create_shop_view_partial, shop_detail_view, shop_add_review_view

app_name = "shop"

urlpatterns = [
    path('create_shop', create_shop_view, name='create_shop'),
    path('create_shop_partial', create_shop_view_partial, name='create_shop_partial'),
    path('my_shop', my_shop_view, name='my_shop'),
    path('shop_detail/<str:name>', shop_detail_view, name='shop_detail'),
    path('shop/add_review', shop_add_review_view, name='shop_add_review'),
]