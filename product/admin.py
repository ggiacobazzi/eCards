from django.contrib import admin

# Register your models here.
from product.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'title', 'shop', 'quantity', 'price', 'shipment', 'date')
    search_fields = ('title', 'shop', 'quantity', 'price')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Product, ProductAdmin)
