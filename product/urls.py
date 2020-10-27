from django.urls import path
from product.views import add_product_view, finalize_new_product_view, ProductChange, \
    remove_product_view, send_product_view

app_name = "product"

urlpatterns = [
    path('add_new_product', add_product_view, name='add_new_product'),
    path('finalize_new_product/<str:prod_id>', finalize_new_product_view, name='finalize_new_product'),
    path('edit_product/<int:pk>', ProductChange.as_view(), name='edit_product'),
    path('remove_product/', remove_product_view, name='remove_product'),
    path('send_product', send_product_view, name='send_product'),
]
