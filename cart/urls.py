from django.urls import path

from cart.views import add_to_cart_view, cart_summary_view, delete_from_cart_view, \
    checkout_view

app_name = 'shopping_cart'

urlpatterns = [
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('cart_summary/', cart_summary_view, name='cart_summary'),
    path('cart_delete_item/', delete_from_cart_view, name='delete_from_cart'),
    path('checkout/', checkout_view, name='checkout'),
]
