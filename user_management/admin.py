from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from user_management.models import CustomUser


class AccountAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'email', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_vendor')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(CustomUser, AccountAdmin)
