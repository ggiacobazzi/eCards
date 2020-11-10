from django.contrib import admin

# Register your models here.
from cart.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_ordered', 'is_sent', 'date_ordered')
    search_fields = ('user', 'is_sent')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Order, OrderAdmin)


