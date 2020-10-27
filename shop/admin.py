from django.contrib import admin

# Register your models here.
from shop.models import Shop


class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('user', 'name')
    readonly_fields = ['opening_date']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Shop, ShopAdmin)
