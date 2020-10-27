from django.db import models

# Create your models here.
from product.models import Product
from shop.models import Shop
from user_management.models import CustomUser


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(null=True)
    final_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return self.product.title


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)
    shipping_address = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=60)
    credit_card_number = models.IntegerField(null=True)
    cvv = models.IntegerField(null=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def get_shipment_cost(self):
        return sum([item.product.shipment for item in self.items.all()])

    def get_total_price(self):
        return self.get_cart_total() + self.get_shipment_cost()




